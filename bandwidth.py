#!/usr/bin/env python3

import requests
from getpass import getpass
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
import common


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


def plot_24h_average_bandwidth(df, nanopi_names=None, plot_name='24h_average_bandwidth.svg',
                            title="Average Bandwidth by Hour for All NanoPi's"):
    """Produces a graph depicting average bandwidth over all nanopis by hour of day for up and another for down"""
    # up
    by_hour = df.loc[(slice(None), slice(None), 'up'), 'bandwidth'].groupby(by=(lambda x: x[0].hour)).mean()
    ax = by_hour.plot()
    ax.set(xlabel='Hour of Day', ylabel='Bandwidth (Mbit/s)', title=title)
    fig = ax.get_figure()
    fig.savefig(plot_name)
    # down


def plot_24h_bandwidth(df, nanopi_names=None, plot_name='24h_bandwidth.svg',
                    title="Average Bandwidth by Hour", chart_width=10):
    """Produces a graph showing the average hourly bandwidth for each nanopi"""
    by_hour = df.loc[:, 'bandwidth'].unstack().groupby(by=(lambda x: x.hour)).mean()
    labels = []
    for nanopi_id in by_hour.columns:
        labels.append(nanopi_names.get(nanopi_id))
    ax = by_hour.plot()
    ax.set(xlabel='Hour of Day', ylabel='Bandwidth (Mbit/s)', title=title)
    if nanopi_names:
        ax.legend(labels)
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
