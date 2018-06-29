#!/usr/bin/env python3

# Contains plotting functions related to ping test results.

import requests
from getpass import getpass
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import common


def plot_down_count(df, nanopi_names=None, plot_name='down_count.svg',
                    title='Number of Failed Pings', chart_width=10):
    """Produces a bar graph depicting number of failed pings in given dataframe

    Arguments:
    df - the pandas dataframe used as a data source
    nanopi_names - a dict where the keys are nanopi IDs and the values are the names you want on the plot
    plot_name - the file name of the plot that is produced by this function
    title - a string that will become the title of the produced plot
    chart_width - the width of the produced plot
    """
    counts = df.loc[:, 'state'].groupby('nanopi').count()
    ax = counts.plot(kind='bar')
    ax.set(xlabel='Location', ylabel='Failed Ping Count', title=title)
    if nanopi_names:
        labels = []
        for nanopi_id in counts.index:
            labels.append(nanopi_names.get(nanopi_id))
        ax.set_xticklabels(labels, rotation=0)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig(plot_name)
    fig.clear()


if __name__ == '__main__':

    username = input("API Username: ")
    password = getpass(prompt="API Password: ")
    auth = requests.auth.HTTPBasicAuth(username, password)

    nanopis = requests.get(common.NANOPI_URL, auth=auth).json()
    nanopi_names = {nanopi.get('id'):nanopi.get('location_info') for nanopi in nanopis}

    df = common.get_ping_dataframe(auth)
    plot_down_count(df, nanopi_names=nanopi_names)

#    df_wo_demetrios = df.loc[(slice(None), [11, 12, 13, 14, 17], slice(None)), :]
#    plot_average(df_wo_demetrios, nanopi_names, plot_name='average_bandwidth_wo_demetrios.svg',
#                 title='Average Bandwidth by Location (without Demetrios)')
#    plot_24h_average(df_wo_demetrios)
#    plot_24h(df_wo_demetrios, nanopi_names=nanopi_names)
