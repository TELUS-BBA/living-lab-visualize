#!/usr/bin/env python3

import requests
from getpass import getpass
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
import json
from common import get_from_api


def get_bandwidth_dataframe(auth=None, params=None):

    base_url = "http://localhost:5000"
    iperf3_url = "{}/iperf3/".format(base_url)

    if not auth:
        username = input("API Username: ")
        password = getpass(prompt="API Password: ")
        auth = requests.auth.HTTPBasicAuth(username, password)

    # get list of results from API with given parameters
    print("Getting raw data from API...")
    results = get_from_api(iperf3_url, auth, params)

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


if __name__ == '__main__':

    df2 = get_bandwidth_dataframe()






