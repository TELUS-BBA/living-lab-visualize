#!/usr/bin/env python3

import requests


BASE_URL = "http://localhost:5000"
NANOPI_URL = "{}/nanopi/".format(BASE_URL)
IPERF3_URL = "{}/iperf3/".format(BASE_URL)
JITTER_URL = "{}/jitter/".format(BASE_URL)
LATENCY_URL = "{}/sockperf/".format(BASE_URL)
PING_URL = "{}/ping/".format(BASE_URL)


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
