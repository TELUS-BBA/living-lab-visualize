#!/usr/bin/env python3

import requests
from getpass import getpass
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
import common


def plot_average_jitter(df, nanopi_names=None, plot_name='average_jitter.svg',
                        title='Average Jitter by Location', chart_width=10):
    """Produces a graph showing average jitter over entire trial for each nanopi"""
    averages = df.loc[:, 'jitter'].groupby(['nanopi']).mean()
    ax = averages.plot(kind='bar')
    ax.set(xlabel='Location', ylabel='Jitter (ms)', title=title)
    if nanopi_names:
        labels = []
        for nanopi_id in averages.index:
            labels.append(nanopi_names.get(nanopi_id))
        ax.legend(labels)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig(plot_name)


def plot_24h_average_jitter(df, nanopi_names=None, plot_name='24h_average_jitter.svg',
                            title="Average Jitter by Hour (Aggregate)", chart_width=10):
    """Produces a graph depicting average jitter over all nanopis by hour of day"""
    by_hour = df.loc[:, 'jitter'].groupby(by=(lambda x: x[0].hour)).mean()
    ax = by_hour.plot()
    ax.set(xlabel='Hour of Day', ylabel='Jitter (ms)', title=title)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig(plot_name)


def plot_24h_jitter(df, nanopi_names=None, plot_name='24h_jitter.svg',
                    title="Average Jitter by Hour (Individual)", chart_width=10):
    """Produces a graph showing the average hourly jitter for each nanopi"""
    by_hour = df.loc[:, 'jitter'].unstack().groupby(by=(lambda x: x.hour)).mean()
    ax = by_hour.plot()
    ax.set(xlabel='Hour of Day', ylabel='Jitter (ms)', title=title)
    if nanopi_names:
        labels = []
        for nanopi_id in by_hour.columns:
            labels.append(nanopi_names.get(nanopi_id))
        ax.legend(labels)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig(plot_name)


def plot_dow_average_jitter(df, plot_name='dow_average_jitter.svg',
                            title="Average Jitter by Day of Week (Aggregate)", chart_width=10):
    """Produces a graph showing the average aggregated jitter for all nanopis by day of week

    A little messed up for the trial because we're missing data for Wednesday.
    """
    by_dow = df.loc[:, 'jitter'].groupby(by=(lambda x: x[0].dayofweek)).mean().reindex(range(7))
    ax = by_dow.plot(kind='bar')
    dows = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ax.set_xticklabels(dows, rotation=0)
    ax.set(xlabel='Day of Week', ylabel='Jitter (ms)', title=title)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig(plot_name)


def plot_dow_jitter(df, nanopi_names=None, plot_name='dow_jitter.svg',
                    title="Average Jitter by Day of Week (Individual)", chart_width=10):
    """Produces a graph depicting the average individual jitter for each nanopi by day of week"""
    by_dow = df.loc[:, 'jitter'].unstack().groupby(by=(lambda x: x.dayofweek)).mean().reindex(range(7))
    ax = by_dow.plot()
    # the _ is not shown because 0th element goes at origin but there is no xtick at origin
    dows = ['_', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ax.set_xticklabels(dows, rotation=0)
    ax.set(xlabel='Day of Week', ylabel='Jitter (ms)', title=title)
    if nanopi_names:
        labels = []
        for nanopi_id in by_dow.columns:
            labels.append(nanopi_names.get(nanopi_id))
        ax.legend(labels)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig(plot_name)


def coverage(df, nanopi_names=None, plot_name='coverage_jitter.svg',
             title="Coverage of Jitter Tests", chart_width=10):
    pass


if __name__ == '__main__':

    username = input("API Username: ")
    password = getpass(prompt="API Password: ")
    auth = requests.auth.HTTPBasicAuth(username, password)

    nanopis = requests.get(common.NANOPI_URL, auth=auth).json()
    nanopi_names = {nanopi.get('id'):nanopi.get('location_info') for nanopi in nanopis}

    df = common.get_jitter_dataframe(auth)
#    plot_average_jitter(df, nanopi_names=nanopi_names)
#    plot_24h_average_jitter(df)
#    plot_24h_jitter(df, nanopi_names=nanopi_names)
    plot_dow_average_jitter(df)
    plot_dow_jitter(df, nanopi_names=nanopi_names)
