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


def ingest_results(results, datetime_field='upload_date'):

    ingested_results = []
    for result in results:
        ingested_result = result.copy()
        maya_time = maya.parse(result.get(datetime_field))
        ingested_result[datetime_field] = maya_time
        ingested_results.append(ingested_result)

    return ingested_results


def get_coverage(results, datetime_field='upload_date'):
    """Takes a list of dicts, each of which must contain a MayaDT object as the value under the key
    'upload_date', and checks for hourly gaps in the data. Returns a list of dicts containing the
    MayaDT and whether an element was present for that MayaDT's hour."""

    interval = timedelta(hours=1)
    start = results[0].get(datetime_field)
    end = results[len(results) - 1].get(datetime_field).add(hours=1)
    #end = results[len(results) - 1].get(datetime_field)
    tests = list(maya.intervals(start=start, end=end, interval=interval))

    print(results[len(results) - 1].get(datetime_field).rfc2822())
    print(results[len(results) - 1].get(datetime_field).add(hours=1).rfc2822())

    print("first tests hour: {}".format(tests[0].hour))
    print("first results hour: {}".format(results[0].get(datetime_field).hour))

    print("final tests hour: {}".format(tests[len(tests) - 1].hour))
    print("final results hour: {}".format(results[len(results) - 1].get(datetime_field).hour))

    print("final day: {}".format(tests[len(tests) - 1].rfc2822()))

    results_index = 0
    test_coverage = []
    print("results length: {}".format(len(results)))
    print("tests length: {}".format(len(tests)))
    print("-------------------")
    for i, test in enumerate(tests):
        try:
            if test.hour == results[results_index].get(datetime_field).hour:
                test_coverage.append({datetime_field: test, 'tested': True})
                results_index = results_index + 1
            else:
                test_coverage.append({datetime_field: test, 'tested': False})
        except IndexError:
            pass

    return test_coverage


def test_coverage(file, username=None, password=None):
    """Generates a figure that lets us visualize where tests were missed"""

    base_url = "http://localhost:5000"
    nanopi_url = "{}/nanopi/".format(base_url)
    iperf3_url = "{}/iperf3/".format(base_url)
    jitter_url = "{}/jitter/".format(base_url)
    sockperf_url = "{}/sockperf/".format(base_url)

    if not username:
        username = input("API Username: ")
    if not password:
        password = getpass(prompt="API Password: ")
    auth = requests.auth.HTTPBasicAuth(username, password)

    params = {
        'nanopi': 14,
        #'direction': 'down',
    }
    results = get_from_api(iperf3_url, auth, params)

    ingested_results = ingest_results(results)

    coverage = get_coverage(ingested_results)
    total_tests = len(coverage)
    missed_tests = [test for test in coverage if not test.get('tested')]
    print("Out of {} tests, {} were missed".format(total_tests, len(missed_tests)))
    print("Missed tests:")
    for test in missed_tests:
        print(test.get('upload_date').rfc2822())

    localized_results = localize(coverage, 'America/Edmonton')

    data = [[result.get('tested') for result in localized_results],]

    figure, axis = plot.subplots()
    axis.imshow(data, aspect='auto', cmap=plot.cm.gray, interpolation='nearest')
    axis.set_xlabel("Date")
    #axis.set_ylabel("")
    axis.set_title("Intense Test Coverage")
    #axis.set_xticks([a + bar_width / 2 for a in index])
    #axis.set_xticklabels(labels)
    figure.savefig(file)


def bandwidth_summary_all(file, username=None, password=None):

    base_url = "http://localhost:5000"
    nanopi_url = "{}/nanopi/".format(base_url)
    iperf3_url = "{}/iperf3/".format(base_url)

    if not username:
        username = input("API Username: ")
    if not password:
        password = getpass(prompt="API Password: ")
    auth = requests.auth.HTTPBasicAuth(username, password)

    params = None
    nanopis = requests.get(nanopi_url, auth=auth).json()
    bandwidths = []
    for nanopi in nanopis:
        print("Doing nanopi {}".format(nanopi.get('id')))
        params = {'nanopi': nanopi.get('id'), 'direction': 'up'}
        results = get_from_api(iperf3_url, auth, params)
        up_bandwidths = [result.get('bandwidth') for result in results]
        mean_up_bandwidth = mean(up_bandwidths)
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


def jitter_summary_all(file, username=None, password=None):

    base_url = "http://localhost:5000"
    nanopi_url = "{}/nanopi/".format(base_url)
    jitter_url = "{}/jitter/".format(base_url)

    if not username:
        username = input("API Username: ")
    if not password:
        password = getpass(prompt="API Password: ")
    auth = requests.auth.HTTPBasicAuth(username, password)

    params = None
    nanopis = requests.get(nanopi_url, auth=auth).json()
    jitters = []
    for nanopi in nanopis:
        print("Doing nanopi {}".format(nanopi.get('id')))
        params = {'nanopi': nanopi.get('id')}
        results = get_from_api(jitter_url, auth, params)
        result_jitters = [result.get('jitter') for result in results]
        mean_jitter = mean(result_jitters)
        jitters.append({
            'nanopi': nanopi.get('id'),
            'location': nanopi.get('location_info'),
            'jitter': mean_jitter,
        })

    for jitter in jitters:
        print("At {} average jitter is {} ms".format(
            jitter.get('location'),
            jitter.get('jitter'),
        ))

    bar_width = 0.4
    opacity = 0.6
    figure, axis = plot.subplots()

    index = range(len(jitters))
    labels = [jitter.get('location') for jitter in jitters]
    mean_jitter = [jitter.get('jitter') for jitter in jitters]

    rect = axis.bar(index, mean_jitter, bar_width, alpha=opacity)
    axis.set_xlabel("Location")
    axis.set_ylabel("Jitter (ms)")
    axis.set_title("Average Jitter by Location")
    axis.set_xticks(index)
    axis.set_xticklabels(labels)
    figure.set_size_inches(9, 6)
    figure.savefig(file)


def latency_summary_all(file, username=None, password=None):

    base_url = "http://localhost:5000"
    nanopi_url = "{}/nanopi/".format(base_url)
    sockperf_url = "{}/sockperf/".format(base_url)

    if not username:
        username = input("API Username: ")
    if not password:
        password = getpass(prompt="API Password: ")
    auth = requests.auth.HTTPBasicAuth(username, password)

    params = None
    nanopis = requests.get(nanopi_url, auth=auth).json()
    latencies = []
    for nanopi in nanopis:
        print("Doing nanopi {}".format(nanopi.get('id')))
        params = {'nanopi': nanopi.get('id')}
        results = get_from_api(sockperf_url, auth, params)
        result_latencies = [result.get('latency') for result in results]
        mean_latency = mean(result_latencies)
        latencies.append({
            'nanopi': nanopi.get('id'),
            'location': nanopi.get('location_info'),
            'latency': mean_latency/1000,
        })

    for latency in latencies:
        print("At {} average one-way latency is {} ms".format(
            latency.get('location'),
            latency.get('latency'),
        ))

    bar_width = 0.4
    opacity = 0.6
    figure, axis = plot.subplots()

    index = range(len(latencies))
    labels = [latency.get('location') for latency in latencies]
    mean_latency = [latency.get('latency') for latency in latencies]

    rect = axis.bar(index, mean_latency, bar_width, alpha=opacity)
    axis.set_xlabel("Location")
    axis.set_ylabel("Latency (ms)")
    axis.set_title("Average One-Way Latency by Location")
    axis.set_xticks(index)
    axis.set_xticklabels(labels)
    figure.set_size_inches(9, 6)
    figure.savefig(file)



        


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

    #username = input("API Username: ")
    #password = getpass(prompt="API Password: ")

    #bandwidth_summary_all('bandwidth.svg', username=username, password=password)
    #jitter_summary_all('jitter.svg', username=username, password=password)
    #latency_summary_all('latency.svg', username=username, password=password)
    test_coverage('coverage.svg')

#    data = np.random.random((20, 500)) > .2
#    print(len(data))
#    print(len(data[0]))
