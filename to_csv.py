#!/usr/bin/env python3

# Pulls data from the API (not directly from the sqlite database),
# formats/processes it, and writes it to /home/ubuntu/data/ .

import os
import datetime
import requests
import pandas as pd
from common import (
    get_bandwidth_dataframe,
    get_jitter_dataframe,
    get_latency_dataframe,
    get_nanopi_list,
)

with open('log.txt', 'at') as file:
    file.write("Ran at {}\n".format(datetime.datetime.now()))

data_dir = '/home/ubuntu/data'
username = "admin"
password = "Atmop*8twtiwytd"
auth = requests.auth.HTTPBasicAuth(username, password)

pd.DataFrame(get_nanopi_list(auth)).to_csv(os.path.join(data_dir, 'nanopis.csv'))
get_bandwidth_dataframe(auth).to_csv(os.path.join(data_dir, 'bandwidth.csv'))
get_jitter_dataframe(auth).to_csv(os.path.join(data_dir, 'jitter.csv'))
get_latency_dataframe(auth).to_csv(os.path.join(data_dir, 'latency.csv'))
