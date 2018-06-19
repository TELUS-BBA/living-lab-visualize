#!/usr/bin/env python3

import requests
from common import get_bandwidth_dataframe, get_jitter_dataframe
import bandwidth
import jitter

username = input("API Username: ")
password = getpass(prompt="API Password: ")
auth = requests.auth.HTTPBasicAuth(username, password)

nanopis = requests.get(common.NANOPI_URL, auth=auth).json()
nanopis.raise_for_status()
nanopi_names = {nanopi.get('id'):nanopi.get('location_info') for nanopi in nanopis}

df = common.get_bandwidth_dataframe(auth)
plot_average_bandwidth(df, nanopi_names)
df_wo_demetrios = df.loc[(slice(None), [11, 12, 13, 14, 17], slice(None)), :]
plot_average_bandwidth(df_wo_demetrios, nanopi_names, plot_name='average_bandwidth_wo_demetrios.svg',
                       title='Average Bandwidth by Location (without Demetrios)')
plot_24h_average_bandwidth(df_wo_demetrios)


df = common.get_jitter_dataframe(auth)
plot_average_jitter(df, nanopi_names=nanopi_names)
plot_24h_average_jitter(df)
plot_24h_jitter(df, nanopi_names=nanopi_names)
