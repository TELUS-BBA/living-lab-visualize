#!/usr/bin/env python3

import requests
from getpass import getpass
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plot
import numpy as np
from statistics import mean
import maya
from datetime import timedelta
from copy import copy

from common import get_data


BASE_URL = "http://localhost:5000"
NANOPI_URL = "{}/nanopi/".format(BASE_URL)
IPERF3_URL = "{}/iperf3/".format(BASE_URL)


def compare_average_bandwidth(file, nanopis, username, password):
    """Generate a chart that compares the bandwidth results of the given list of nanopis.
    
    Arguments:
    file - the file name that the chart will be saved into, for example 'bandwidth.svg'
    nanopis - a list of nanopi dicts as given in the REST API
    username - the HTTP basic auth username that lets you access the API
    password - the HTTP basic auth password that lets you access the API
    """
    auth = requests.auth.HTTPBasicAuth(username, password)

    bandwidths = []
    for nanopi in nanopis:
        print("Fetching data for nanopi {}".format(nanopi.get('id')))

        # get average up bandwidth for nanopi
        params = {
            'nanopi': nanopi.get('id'),
            'direction': 'up',
        }
        up_results = get_from_api(IPERF3_URL, auth, params)
        up_bandwidths = [result.get('bandwidth') for result in up_results]
        mean_up_bandwidth = mean(up_bandwidths)

        # get average down bandwidth for nanopi
        params = {'nanopi': nanopi.get('id'), 'direction': 'down'}
        results = get_from_api(iperf3_url, auth, params)
        down_bandwidths = [result.get('bandwidth') for result in results]
        mean_down_bandwidth = mean(down_bandwidths)

        bandwidths.append({
            'nanopi': nanopi.get('id'),
            'location': nanopi.get('location_info'),
            'up': mean_up_bandwidth,
            'down': mean_down_bandwidth,
        })

    # report average bandwidths for each nanopi
    for bandwidth in bandwidths:
        print("At {} average up is {} Mbit/s and average down is {} Mbit/s".format(
            bandwidth.get('location'),
            round(bandwidth.get('up')),
            round(bandwidth.get('down'))
        ))

    bar_width = 0.4
    opacity = 0.6
    figure, axis = plot.subplots()

    index = range(len(bandwidths))
    labels = [bandwidth.get('location') for bandwidth in bandwidths]
    means_up = [bandwidth.get('up') for bandwidth in bandwidths]
    means_down = [bandwidth.get('down') for bandwidth in bandwidths]

    rects_up = axis.bar(index, means_up, bar_width, label='Up', color='r', alpha=opacity)
    rects_down = axis.bar([a + bar_width for a in index], means_down,
                          bar_width, label='Down', color='b', alpha=opacity)
    axis.set_xlabel("Location")
    axis.set_ylabel("Bandwidth (Mbit/s)")
    axis.set_title("Average Bandwidth by Location")
    axis.set_xticks([a + bar_width / 2 for a in index])
    axis.set_xticklabels(labels)
    axis.legend()
    figure.set_size_inches(12, 6)
    figure.savefig(file)


def average_bandwidth_per_hour(file, nanopis, username, password):
    """Generate a chart that shows the bandwidth per hour for an average of the given list of nanopis.
    
    Arguments:
    file - the file name that the chart will be saved into, for example 'bandwidth.svg'
    nanopis - a list of nanopi dicts as given in the REST API
    username - the HTTP basic auth username that lets you access the API
    password - the HTTP basic auth password that lets you access the API
    """
    auth = requests.auth.HTTPBasicAuth(username, password)

    # get up data
    up_data = {hour: [] for hour in range(24)}
    for nanopi in nanopis:
        print("Fetching data for nanopi {}".format(nanopi.get('id')))
        params = {
            'nanopi': nanopi.get('id'),
            'direction': 'up',
        }
        results = get_data(IPERF3_URL, auth, params)
        for result in results:
            up_data[result.get('upload_date').hour].append(result.get('bandwidth'))

    for key, value in up_data.items():
        up_data[key] = mean(value)
        print("Hour {}: {} Mbit/s".format(key, round(up_data[key])))

    # get down data
    down_data = {hour: [] for hour in range(24)}
    for nanopi in nanopis:
        print("Fetching data for nanopi {}".format(nanopi.get('id')))
        params = {
            'nanopi': nanopi.get('id'),
            'direction': 'down',
        }
        results = get_data(IPERF3_URL, auth, params)
        for result in results:
            down_data[result.get('upload_date').hour].append(result.get('bandwidth'))

    for key, value in down_data.items():
        down_data[key] = mean(value)
        print("Hour {}: {} Mbit/s".format(key, round(down_data[key])))

    # plot data
    
#    figure, axis = plot.subplots()
#    axis.plot()
#    axis.set(xlabel='Hour of Day', ylabel='Bandwidth (Mbit/s)', title='About as simple as it gets')
#    axis.grid()
#    figure.savefig('graph.svg')


def each_bandwidth_per_hour(file, nanopis, username, password):
    pass

def bandwidth_over_time_period(file, nanopis, username, password):
    pass


#params = {
#    'nanopi': 12,
#    'direction': 'down'
#}
#results = get_from_api(iperf3_url, auth, params)
#
#bandwidth = [result.get('bandwidth') for result in results]
#
#figure, axis = plot.subplots()
#axis.plot(bandwidth)
#axis.set(xlabel='time', ylabel='bandwidth (Mbit/s)', title='About as simple as it gets')
#axis.grid()
#figure.savefig('graph.svg')

if __name__ == '__main__':

    username = input("API Username: ")
    password = getpass(prompt="API Password: ")
    auth = requests.auth.HTTPBasicAuth(username, password)

    nanopis = requests.get(NANOPI_URL, auth=auth).json()

#    compare_average_bandwidth('bandwidth.svg', username, password)
    average_bandwidth_per_hour('bandwidth.svg', nanopis, username, password)
