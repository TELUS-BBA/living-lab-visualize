#!/usr/bin/env python3

import requests
from getpass import getpass
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
import common


def plot_average(df, nanopi_names=None, plot_name='average_latency.svg',
                        title='Average Latency by Location', chart_width=10):
    """Produces a graph showing average latency over entire trial for each nanopi"""
    averages = df.loc[:, 'latency'].groupby(['nanopi']).mean()
    ax = averages.plot(kind='bar')
    ax.set(xlabel='Location', ylabel='Latency (ms)', title=title)
    if nanopi_names:
        labels = []
        for nanopi_id in averages.index:
            labels.append(nanopi_names.get(nanopi_id))
        ax.set_xticklabels(labels, rotation=0)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig(plot_name)
    fig.clear()


def plot_24h_average(df, nanopi_names=None, plot_name='24h_average_latency.svg',
                            title="Average Latency by Hour (Aggregate)", chart_width=10):
    """Produces a graph depicting average latency over all nanopis by hour of day"""
    by_hour = df.loc[:, 'latency'].groupby(by=(lambda x: x[0].hour)).mean()
    ax = by_hour.plot()
    ax.set(xlabel='Hour of Day', ylabel='Latency (ms)', title=title)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig(plot_name)
    fig.clear()


def plot_24h(df, nanopi_names=None, plot_name='24h_latency.svg',
                    title="Average Latency by Hour (Individual)", chart_width=10):
    """Produces a graph showing the average hourly latency for each nanopi"""
    by_hour = df.loc[:, 'latency'].unstack().groupby(by=(lambda x: x.hour)).mean()
    ax = by_hour.plot()
    ax.set(xlabel='Hour of Day', ylabel='Latency (ms)', title=title)
    if nanopi_names:
        labels = []
        for nanopi_id in by_hour.columns:
            labels.append(nanopi_names.get(nanopi_id))
        ax.legend(labels)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig(plot_name)
    fig.clear()


def plot_dow_average(df, plot_name='dow_average_latency.svg',
                            title="Average Latency by Day of Week (Aggregate)", chart_width=10):
    """Produces a graph showing the average aggregated latency for all nanopis by day of week

    A little messed up for the trial because we're missing data for Wednesday.
    """
    by_dow = df.loc[:, 'latency'].groupby(by=(lambda x: x[0].dayofweek)).mean().reindex(range(7))
    ax = by_dow.plot()
    dows = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ax.set_xticklabels(dows, rotation=0)
    ax.set(xlabel='Day of Week', ylabel='Latency (ms)', title=title)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig(plot_name)
    fig.clear()


def plot_dow(df, nanopi_names=None, plot_name='dow_latency.svg',
                    title="Average Latency by Day of Week (Individual)", chart_width=10):
    """Produces a graph depicting the average individual latency for each nanopi by day of week"""
    by_dow = df.loc[:, 'latency'].unstack().groupby(by=(lambda x: x.dayofweek)).mean().reindex(range(7))
    ax = by_dow.plot()
    # the _ is not shown because 0th element goes at origin but there is no xtick at origin
    dows = ['_', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ax.set_xticklabels(dows, rotation=0)
    ax.set(xlabel='Day of Week', ylabel='Latency (ms)', title=title)
    if nanopi_names:
        labels = []
        for nanopi_id in by_dow.columns:
            labels.append(nanopi_names.get(nanopi_id))
        ax.legend(labels)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig(plot_name)
    fig.clear()


def coverage(df, nanopi_names=None, plot_name='coverage_latency.svg',
             title="Coverage of Latency Tests", chart_width=10):
    pass


if __name__ == '__main__':

    username = input("API Username: ")
    password = getpass(prompt="API Password: ")
    auth = requests.auth.HTTPBasicAuth(username, password)

    nanopis = requests.get(common.NANOPI_URL, auth=auth).json()
    nanopi_names = {nanopi.get('id'):nanopi.get('location_info') for nanopi in nanopis}

    df = common.get_latency_dataframe(auth)
    plot_average(df, nanopi_names=nanopi_names)
    plot_24h_average(df)
    plot_24h(df, nanopi_names=nanopi_names)
    plot_dow_average(df)
    plot_dow(df, nanopi_names=nanopi_names)
