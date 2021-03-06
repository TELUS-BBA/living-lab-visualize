#!/usr/bin/env python3

# Contains plotting functions related to jitter test results.

import requests
from getpass import getpass
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
#import matplotlib.dates as dates
import common


def plot_average(df, nanopi_names=None, plot_name='average_jitter.svg',
                 title='Average Jitter by Location', chart_width=10):
    """Produces a graph showing average jitter over entire trial for each NanoPi.

    Arguments:
    df - the pandas dataframe used as a data source
    nanopi_names - a dict where the keys are nanopi IDs and the values are the names you want on the plot
    plot_name - the file name of the plot that is produced by this function
    title - a string that will become the title of the produced plot
    chart_width - the width of the produced plot
    """
    averages = df.loc[:, 'jitter'].groupby(['nanopi']).mean()
    ax = averages.plot(kind='bar')
    ax.set(xlabel='Location', ylabel='Jitter (ms)', title=title)
    if nanopi_names:
        labels = []
        for nanopi_id in averages.index:
            labels.append(nanopi_names.get(nanopi_id))
        ax.set_xticklabels(labels, rotation=0)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig(plot_name)
    fig.clear()


def plot_24h_average(df, nanopi_names=None, plot_name='24h_average_jitter.svg',
                     title="Average Jitter by Hour (Aggregate)", chart_width=10):
    """Produces a graph depicting average jitter over all NanoPis by hour of day.

    Arguments:
    df - the pandas dataframe used as a data source
    nanopi_names - a dict where the keys are nanopi IDs and the values are the names you want on the plot
    plot_name - the file name of the plot that is produced by this function
    title - a string that will become the title of the produced plot
    chart_width - the width of the produced plot
    """
    by_hour = df.loc[:, 'jitter'].groupby(by=(lambda x: x[0].hour)).mean()
    ax = by_hour.plot()
    ax.set(xlabel='Hour of Day', ylabel='Jitter (ms)', title=title)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig(plot_name)
    fig.clear()


def plot_24h(df, nanopi_names=None, plot_name='24h_jitter.svg',
             title="Average Jitter by Hour (Individual)", chart_width=10):
    """Produces a graph showing the average hourly jitter for each NanoPi.

    Arguments:
    df - the pandas dataframe used as a data source
    nanopi_names - a dict where the keys are nanopi IDs and the values are the names you want on the plot
    plot_name - the file name of the plot that is produced by this function
    title - a string that will become the title of the produced plot
    chart_width - the width of the produced plot
    """
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
    fig.clear()


def plot_dow_average(df, plot_name='dow_average_jitter.svg',
                     title="Average Jitter by Day of Week (Aggregate)", chart_width=10):
    """Produces a graph showing the average aggregated jitter for all nanopis by day of week.

    Arguments:
    df - the pandas dataframe used as a data source
    plot_name - the file name of the plot that is produced by this function
    title - a string that will become the title of the produced plot
    chart_width - the width of the produced plot
    """
    by_dow = df.loc[:, 'jitter'].groupby(by=(lambda x: x[0].dayofweek)).mean().reindex(range(7))
    ax = by_dow.plot()
    dows = ['_', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ax.set_xticklabels(dows, rotation=0)
    ax.set(xlabel='Day of Week', ylabel='Jitter (ms)', title=title)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig(plot_name)
    fig.clear()


def plot_dow(df, nanopi_names=None, plot_name='dow_jitter.svg',
             title="Average Jitter by Day of Week (Individual)", chart_width=10):
    """Produces a graph depicting the average individual jitter for each nanopi by day of week.

    Arguments:
    df - the pandas dataframe used as a data source
    nanopi_names - a dict where the keys are nanopi IDs and the values are the names you want on the plot
    plot_name - the file name of the plot that is produced by this function
    title - a string that will become the title of the produced plot
    chart_width - the width of the produced plot
    """
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
    fig.clear()


def plot_all_average(df, plot_name='all_average_jitter.svg',
                     title="Jitter over Entire Trial (Aggregate)", chart_width=10):
    """Use when you want to plot the average of multiple locations each hour over unlimited time.

    Arguments:
    df - the pandas dataframe used as a data source
    plot_name - the file name of the plot that is produced by this function
    title - a string that will become the title of the produced plot
    chart_width - the width of the produced plot
    """
    averages = df.loc[:, 'jitter'].groupby('datetime').mean()
    ax = averages.plot()
    ax.set(xlabel='Date', ylabel='Jitter (ms)', title=title)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig(plot_name)
    fig.clear()


def plot_all(df, nanopi_names=None, plot_name='all_jitter.svg',
             title="Jitter over Entire Trial (Individual)", chart_width=10):
    """Plots every datapoint for each individual nanopi that you give it.

    Arguments:
    df - the pandas dataframe used as a data source
    nanopi_names - a dict where the keys are nanopi IDs and the values are the names you want on the plot
    plot_name - the file name of the plot that is produced by this function
    title - a string that will become the title of the produced plot
    chart_width - the width of the produced plot
    """
    data = df.loc[:, 'jitter'].unstack()
    ax = data.plot()
    ax.set(xlabel='Date', ylabel='Jitter (ms)', title=title)
    if nanopi_names:
        labels = []
        for nanopi_id in data.columns:
            labels.append(nanopi_names.get(nanopi_id))
        ax.legend(labels)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig(plot_name)
    fig.clear()


def plot_coverage(df, nanopi_names=None, plot_name='coverage_jitter.svg',
                  title="Coverage of Jitter Tests", chart_width=10):
    """Produces a plot that depicts which jitter tests were missed over the given data.

    Arguments:
    df - the pandas dataframe used as a data source
    nanopi_names - a dict where the keys are nanopi IDs and the values are the names you want on the plot
    plot_name - the file name of the plot that is produced by this function
    title - a string that will become the title of the produced plot
    chart_width - the width of the produced plot
    """
    coverage = df.loc[:, 'jitter'].unstack().fillna(value=False).apply(lambda y: y.apply(lambda x: bool(x)))
#    xtick_dates = set([row.floor('D').toordinal() for row in coverage.index])
    black_patch = mpatches.Patch(color='black', label='missing')
    white_patch = mpatches.Patch(color='white', label='present')
    data = []
    for column_index in range(coverage.shape[1]):
        data.append(list(coverage.iloc[:, column_index]))
    fig, ax = plt.subplots()
    ax.imshow(data, aspect='auto', cmap=plt.cm.gray, interpolation='nearest')
    if nanopi_names:
        labels = []
        for nanopi_id in coverage.columns:
            labels.append(nanopi_names.get(nanopi_id))
        ax.set_yticklabels(['_', *labels])
#    ax.xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
#    ax.xaxis.set_major_locator(dates.DayLocator(bymonthday=range(1, 32)))
#    ax.set_xticks(xtick_dates)
#    ax.set_xticklabels(xtick_dates)
    #ax.set_xticklabels(coverage.index.date)
    #fig.autofmt_xdate()
    #ax.set(xlabel='Date', ylabel='Location', title=title)
    ax.set(ylabel='Location', title=title)
    ax.legend(handles=[black_patch, white_patch])
    fig.set_size_inches(chart_width, 6)
    fig.savefig(plot_name)
    fig.clear()


if __name__ == '__main__':

    username = input("API Username: ")
    password = getpass(prompt="API Password: ")
    auth = requests.auth.HTTPBasicAuth(username, password)

    nanopis = requests.get(common.NANOPI_URL, auth=auth).json()
    nanopi_names = {nanopi.get('id'):nanopi.get('location_info') for nanopi in nanopis}

    df = common.get_jitter_dataframe(auth)
    plot_average(df, nanopi_names=nanopi_names)
    plot_24h_average(df)
    plot_24h(df, nanopi_names=nanopi_names)
    plot_dow_average(df)
    plot_dow(df, nanopi_names=nanopi_names)
    plot_all_average(df)
    plot_all(df, nanopi_names=nanopi_names)
    plot_coverage(df, nanopi_names=nanopi_names)
