#!/usr/bin/env python3

# This file contains example scripts.
# The idea is that you read them as examples while creating your own plots.

import os
import requests
from getpass import getpass
import pandas as pd

import common
import bandwidth
import jitter
import latency
import ping

username = input("API Username: ")
password = getpass(prompt="API Password: ")
auth = requests.auth.HTTPBasicAuth(username, password)

nanopis = common.get_nanopi_list(auth)
nanopi_names = {nanopi.get('id'):nanopi.get('location_info') for nanopi in nanopis}

# bandwidth
print("Creating plots for bandwidth")
df = pd.read_hdf('data/bandwidth.h5', 'df')
bandwidth.plot_average(df, nanopi_names=nanopi_names)
bandwidth.plot_24h_average(df)
bandwidth.plot_24h(df, nanopi_names=nanopi_names)
bandwidth.plot_dow_average(df)
bandwidth.plot_dow(df, nanopi_names=nanopi_names)
bandwidth.plot_all_average(df)
bandwidth.plot_all(df, nanopi_names=nanopi_names)
bandwidth.plot_coverage(df, nanopi_names=nanopi_names)

# jitter
print("Creating plots for jitter")
df = pd.read_hdf('data/jitter.h5', 'df')
jitter.plot_average(df, nanopi_names=nanopi_names)
jitter.plot_24h_average(df)
jitter.plot_24h(df, nanopi_names=nanopi_names)
jitter.plot_dow_average(df)
jitter.plot_dow(df, nanopi_names=nanopi_names)
jitter.plot_all_average(df)
jitter.plot_all(df, nanopi_names=nanopi_names)
jitter.plot_coverage(df, nanopi_names=nanopi_names)

# latency
print("Creating plots for latency")
df = pd.read_hdf('data/latency.h5', 'df')
latency.plot_average(df, nanopi_names=nanopi_names)
latency.plot_24h_average(df)
latency.plot_24h(df, nanopi_names=nanopi_names)
latency.plot_dow_average(df)
latency.plot_dow(df, nanopi_names=nanopi_names)
latency.plot_all_average(df)
latency.plot_all(df, nanopi_names=nanopi_names)
latency.plot_coverage(df, nanopi_names=nanopi_names)

# ping
print("Creating plots for ping")
df = pd.read_hdf('data/ping.h5', 'df')
ping.plot_down_count(df, nanopi_names=nanopi_names)


## ensure plots/ is created
#try:
#    os.mkdir('plots')
#except OSError:
#    pass
#
## bandwidth
#df_bandwidth = common.get_bandwidth_dataframe(auth)
#bandwidth.plot_average(df_bandwidth, nanopi_names=nanopi_names, plot_name='plots/average_bandwidth.svg')
#bandwidth.plot_24h_average(df_bandwidth, plot_name='plots/24h_average_bandwidth.svg')
#bandwidth.plot_24h(df_bandwidth, nanopi_names=nanopi_names, plot_name='plots/24h_bandwidth.svg')
#bandwidth.plot_dow_average(df_bandwidth, plot_name='plots/dow_average_bandwidth.svg')
#bandwidth.plot_dow(df_bandwidth, nanopi_names=nanopi_names, plot_name='plots/dow_bandwidth.svg')
#bandwidth.plot_all_average(df_bandwidth, plot_name='plots/all_average_bandwidth.svg')
#bandwidth.plot_all(df_bandwidth, nanopi_names=nanopi_names, plot_name='plots/all_bandwidth.svg')
#bandwidth.plot_coverage(df_bandwidth, nanopi_names=nanopi_names, plot_name='plots/coverage_bandwidth.svg')
#
## jitter
#df_jitter = common.get_jitter_dataframe(auth)
#jitter.plot_average(df_jitter, nanopi_names=nanopi_names, plot_name='plots/average_jitter.svg')
#jitter.plot_24h_average(df_jitter, plot_name='plots/24h_average_jitter.svg')
#jitter.plot_24h(df_jitter, nanopi_names=nanopi_names, plot_name='plots/24h_jitter.svg')
#jitter.plot_dow_average(df_jitter, plot_name='plots/dow_average_jitter.svg')
#jitter.plot_dow(df_jitter, nanopi_names=nanopi_names, plot_name='plots/dow_jitter.svg')
#jitter.plot_all_average(df_jitter, plot_name='plots/all_average_jitter.svg')
#jitter.plot_all(df_jitter, nanopi_names=nanopi_names, plot_name='plots/all_jitter.svg')
#jitter.plot_coverage(df_jitter, nanopi_names=nanopi_names, plot_name='plots/coverage_jitter.svg')
#
## latency
#df_latency = common.get_latency_dataframe(auth)
#latency.plot_average(df_latency, nanopi_names=nanopi_names, plot_name='plots/average_latency.svg')
#latency.plot_24h_average(df_latency, plot_name='plots/24h_average_latency.svg')
#latency.plot_24h(df_latency, nanopi_names=nanopi_names, plot_name='plots/24h_latency.svg')
#latency.plot_dow_average(df_latency, plot_name='plots/dow_average_latency.svg')
#latency.plot_dow(df_latency, nanopi_names=nanopi_names, plot_name='plots/dow_latency.svg')
#latency.plot_all_average(df_latency, plot_name='plots/all_average_latency.svg')
#latency.plot_all(df_latency, nanopi_names=nanopi_names, plot_name='plots/all_latency.svg')
#latency.plot_coverage(df_latency, nanopi_names=nanopi_names, plot_name='plots/coverage_latency.svg')
#
## ping
#df_ping = common.get_ping_dataframe(auth)
#ping.plot_down_count(df_ping, nanopi_names=nanopi_names, plot_name='plots/down_count.svg')
