#!/usr/bin/env python3

import requests
from getpass import getpass
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
import common


def get_bandwidth_dataframe(auth, params=None):

    # get list of results from API with given parameters
    print("Getting raw data from API...")
    results = common.get_from_api(common.IPERF3_URL, auth, params)

    # put initial multiindex together
    print("Putting initial dataframe together...")
    for result in results:
        result['upload_date'] = pd.Timestamp(result.get('upload_date')).tz_convert('America/Edmonton')
    index_tuples = [[x.get('upload_date').floor('H'), x.get('nanopi'), x.get('direction')] for x in results]
    index = pd.MultiIndex.from_tuples(index_tuples, names=['datetime', 'nanopi', 'direction'])

    # parse bulk of data
    df = pd.DataFrame({'id': [x.get('id') for x in results],
                       'bandwidth': [x.get('bandwidth') for x in results],
                       'upload_date': [x.get('upload_date') for x in results]},
                      index=index)

    # remove duplicates
    print("Removing duplicates...")
    df1 = df.loc[~df.index.duplicated(keep='last'), :]

    # reindex to highlight missing data
    print("Re-indexing dataframe...")
    start = df.index.get_level_values('datetime')[0]
    end = df.index.get_level_values('datetime')[-1]
    iterables = [
        pd.date_range(start, end=end, freq='H'),
        set(df.index.get_level_values('nanopi')),
        ['up', 'down']
    ]
    new_index = pd.MultiIndex.from_product(iterables, names=['datetime', 'nanopi', 'direction'])
    df2 = df1.reindex(index=new_index)

    return df2


def plot_average_bandwidth(df, nanopi_names=None, plot_name='average_bandwidth.svg',
                           title='Average Bandwidth by Location', chart_width=10):
    averages = df.loc[:, 'bandwidth'].groupby(['nanopi', 'direction']).mean().unstack()
    labels = []
    for nanopi_id in averages.index:
        labels.append(nanopi_names.get(nanopi_id))
    ax = averages.plot(kind='bar')
    ax.set(xlabel='Location', ylabel='Bandwidth (Mbit/s)', title=title)
    if nanopi_names:
        ax.set_xticklabels(labels, rotation=0)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig(plot_name)


if __name__ == '__main__':

    username = input("API Username: ")
    password = getpass(prompt="API Password: ")
    auth = requests.auth.HTTPBasicAuth(username, password)

    nanopis = requests.get(common.NANOPI_URL, auth=auth).json()
    nanopi_names = {nanopi.get('id'):nanopi.get('location_info') for nanopi in nanopis}

    df = get_bandwidth_dataframe(auth)
    plot_average_bandwidth(df, nanopi_names)
    df_wo_demetrios = df.loc[(slice(None), [11, 12, 13, 14, 17], slice(None)), :]
    plot_average_bandwidth(df_wo_demetrios, nanopi_names, plot_name='average_bandwidth_wo_demetrios.svg',
                           title='Average Bandwidth by Location (without Demetrios)')
