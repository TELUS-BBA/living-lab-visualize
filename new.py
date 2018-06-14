#!/usr/bin/env python3

import requests
from getpass import getpass
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
import json
from copy import copy


def get_from_api(url, auth, params):
    """Pages through the REST API and retrieves all the data for a certain set of parameters.

    You can treat this as a regular call to requests.get(...).json();
    it abstracts the pagination and gives you the same result you'd get without pagination.
    The arguments more or less mirror those for the requests library.
    See http://docs.python-requests.org/en/master/ for more information.

    Arguments:
    url - the url that will be requested
    auth - the requests auth object; see requests docs
    params - a dict containing URL parameters for the request; see requests docs
    """
    results = []
    response = requests.get(url, auth=auth, params=params)
    response.raise_for_status()
    json = response.json()
    for result in json.get('results'):
        results.append(result)
    url = json.get('next')

    while url:
        response = requests.get(url, auth=auth)
        response.raise_for_status()
        json = response.json()
        for result in json.get('results'):
            results.append(result)
        url = json.get('next')

    return results


def get_bandwidth_dataframe(auth=None, params=None):

    base_url = "http://localhost:5000"
    iperf3_url = "{}/iperf3/".format(base_url)

    if not auth:
        username = input("API Username: ")
        password = getpass(prompt="API Password: ")
        auth = requests.auth.HTTPBasicAuth(username, password)

    # get list of results from API with given parameters
    results = get_from_api(iperf3_url, auth, params)

    # put initial multiindex together
    for result in results:
        result['upload_date'] = pd.Timestamp(result.get('upload_date')).tz_convert('America/Edmonton')
    index_tuples = [[x.get('upload_date').floor('H'), x.get('nanopi'), x.get('direction')] for x in results]
    index = pd.MultiIndex.from_tuples(index_tuples, names=['datetime', 'nanopi', 'direction'])

    # parse bulk of data
    df = pd.DataFrame({'id': [x.get('id') for x in results],
                       'bandwidth': [x.get('bandwidth') for x in results],
                       'upload_date': [x.get('upload_date') for x in results]},
                      index=index)

    # remove duplicates
    df1 = df.loc[~df.index.duplicated(keep='last'), :]

    # reindex to highlight missing data
    start = df.index.get_level_values('datetime')[0]
    end = df.index.get_level_values('datetime')[-1]
    iterables = [
        pd.date_range(start, end=end, freq='H'),
        set(df.index.get_level_values('nanopi')),
        ['up', 'down']
    ]
    new_index = pd.MultiIndex.from_product(iterables, names=['datetime', 'nanopi', 'direction'])
    df2 = df1.reindex(index=new_index)

    return df2


if __name__ == '__main__':

    df2 = get_bandwidth_dataframe()
    print(df2.loc[:,'bandwidth'])






