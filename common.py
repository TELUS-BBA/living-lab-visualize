#!/usr/bin/env python3

import requests
import pandas as pd


BASE_URL = "http://localhost:5000"
NANOPI_URL = "{}/nanopi/".format(BASE_URL)
IPERF3_URL = "{}/iperf3/".format(BASE_URL)
JITTER_URL = "{}/jitter/".format(BASE_URL)
LATENCY_URL = "{}/sockperf/".format(BASE_URL)
PING_URL = "{}/ping/".format(BASE_URL)


def get_from_api(url, auth, params):
    """Pages through the REST API and retrieves all the data for a certain set of parameters.

    Very similar to  a regular call to requests.get(...).json(),
    except that it abstracts the pagination and gives you the same result you'd get without pagination.
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


def get_bandwidth_dataframe(auth, params=None):

    # get list of results from API with given parameters
    print("Getting raw data from API...")
    results = get_from_api(IPERF3_URL, auth, params)

    # put initial multiindex together
    print("Putting initial dataframe together...")
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
    print("Removing duplicates...")
    df1 = df.loc[~df.index.duplicated(keep='last'), :]

    # reindex to highlight missing data
    print("Re-indexing dataframe...")
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


def get_jitter_dataframe(auth, params=None):

    # get list of results from API with given parameters
    print("Getting raw data from API...")
    results = get_from_api(JITTER_URL, auth, params)

    # put initial multiindex together
    print("Putting initial dataframe together...")
    for result in results:
        result['upload_date'] = pd.Timestamp(result.get('upload_date')).tz_convert('America/Edmonton')
    index_tuples = [[x.get('upload_date').floor('H'), x.get('nanopi')] for x in results]
    index = pd.MultiIndex.from_tuples(index_tuples, names=['datetime', 'nanopi'])

    # parse bulk of data
    df = pd.DataFrame({'id': [x.get('id') for x in results],
                       'jitter': [x.get('jitter') for x in results],
                       'upload_date': [x.get('upload_date') for x in results]},
                      index=index)

    # remove duplicates
    print("Removing duplicates...")
    df1 = df.loc[~df.index.duplicated(keep='last'), :]

    # reindex to highlight missing data
    print("Re-indexing dataframe...")
    start = df.index.get_level_values('datetime')[0]
    end = df.index.get_level_values('datetime')[-1]
    iterables = [
        pd.date_range(start, end=end, freq='H'),
        set(df.index.get_level_values('nanopi'))
    ]
    new_index = pd.MultiIndex.from_product(iterables, names=['datetime', 'nanopi'])
    df2 = df1.reindex(index=new_index)

    return df2


def get_latency_dataframe(auth, params=None):

    # get list of results from API with given parameters
    print("Getting raw data from API...")
    results = get_from_api(LATENCY_URL, auth, params)

    # put initial multiindex together
    print("Putting initial dataframe together...")
    for result in results:
        result['upload_date'] = pd.Timestamp(result.get('upload_date')).tz_convert('America/Edmonton')
    index_tuples = [[x.get('upload_date').floor('H'), x.get('nanopi')] for x in results]
    index = pd.MultiIndex.from_tuples(index_tuples, names=['datetime', 'nanopi'])

    # parse bulk of data
    df = pd.DataFrame({'id': [x.get('id') for x in results],
                       'latency': [x.get('latency') for x in results],
                       'upload_date': [x.get('upload_date') for x in results]},
                      index=index)
    df.loc[:, 'latency'] = df.loc[:, 'latency']/1000

    # remove duplicates
    print("Removing duplicates...")
    df1 = df.loc[~df.index.duplicated(keep='last'), :]

    # reindex to highlight missing data
    print("Re-indexing dataframe...")
    start = df.index.get_level_values('datetime')[0]
    end = df.index.get_level_values('datetime')[-1]
    iterables = [
        pd.date_range(start, end=end, freq='H'),
        set(df.index.get_level_values('nanopi'))
    ]
    new_index = pd.MultiIndex.from_product(iterables, names=['datetime', 'nanopi'])
    df2 = df1.reindex(index=new_index)

    return df2


def get_ping_dataframe(auth, params={'state': 'down'}):

    # get list of results from API with given parameters
    print("Getting raw data from API...")
    results = get_from_api(PING_URL, auth, params)

    # put initial multiindex together
    print("Putting initial dataframe together...")
    for result in results:
        result['upload_date'] = pd.Timestamp(result.get('upload_date')).tz_convert('America/Edmonton')
        result['time'] = pd.Timestamp(result.get('time')).tz_convert('America/Edmonton')
    index_tuples = [[x.get('time'), x.get('nanopi')] for x in results]
    index = pd.MultiIndex.from_tuples(index_tuples, names=['datetime', 'nanopi'])

    # parse bulk of data
    df = pd.DataFrame({'id': [x.get('id') for x in results],
                       'state': [x.get('state') for x in results],
                       'upload_date': [x.get('upload_date') for x in results]},
                      index=index)

    return df
