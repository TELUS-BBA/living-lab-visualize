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


def get_from_api(url, auth, params):
    """Pages through the REST API and retrieves all the data for a certain set of parameters.

    Note that the arguments more or less mirror those for the requests library.
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


def ingest(results, datetime_field):
    """Given a list of dicts, converts the time fields into MayaDT objects.

    Arguments:
    results - a list of dicts; each one should contain the key given in datetime_field
    datetime_field - the key of the field in each dict that contains the maya datetime object
    """
    ingested_results = []
    for result in results:
        ingested_result = result.copy()
        maya_time = maya.parse(result.get(datetime_field))
        ingested_result[datetime_field] = maya_time
        ingested_results.append(ingested_result)

    return ingested_results


def localize(results, timezone, datetime_field):
    """Converts time of each dict in list of dicts to a new timezone.
    
    Note that it is assumed that the times in each datetime_field are currently in UTC.
    maya should be used for time objects.

    Arguments:
    results - a list of dicts; each one should contain the key given in datetime_field
    timezone - the timezone that we want to conver the times to
    datetime_field - the key of the field in each dict that contains the maya datetime object
    """
    localized_results = []
    for result in results:
        localized_result = result.copy()
        localized_result[datetime_field] = result[datetime_field].datetime(to_timezone=timezone)
        localized_results.append(localized_result)
    return localized_results


def get_data(url, auth, params, timezone='UTC', datetime_field='upload_date'):
    raw_results = get_from_api(url, auth, params)
    ingested_results = ingest(raw_results, datetime_field=datetime_field)
    localized_results = localize(ingested_results, timezone, datetime_field)
    return localized_results
