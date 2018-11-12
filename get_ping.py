#!/usr/bin/env python3

# Pulls ping data pertaining to a specific date from sqlite database,
# processes it and writes results to file in data/ping/ .

import os
import pandas as pd
import argparse
import sqlite3

def get_ping_count(conn, year, month, day):
    query = 'select * from testresults_pingresult where time between "{year}-{month:02}-{day:02} 00:00:00" and "{year}-{month:02}-{day:02} 23:59:59"'
    print('getting {}-{:02}-{:02}'.format(year, month, day))
    df = pd.read_sql_query(query.format(year=year, month=month, day=day), conn)
    df.loc[:, 'time'] = pd.to_datetime(df.loc[:, 'time'])
    df2 = df.loc[:, ['id', 'nanopi_id', 'state', 'time']].groupby(['nanopi_id', 'state', pd.Grouper(freq='1H', key='time')]).count().unstack(level=1).loc[:, 'id'].fillna(value=0)
    return df2

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-y', dest='year', default=2018, type=int)
    parser.add_argument('-m', dest='month', required=True, type=int)
    parser.add_argument('-d', dest='day', required=True, type=int)
    args = parser.parse_args()

    output_location = 'data/ping/'
    conn = sqlite3.connect('/home/ubuntu/management/app/db.sqlite3')
    df = get_ping_count(conn, args.year, args.month, args.day)
    df.to_csv(os.path.join(output_location, '{}-{:02}-{:02}.csv'.format(args.year, args.month, args.day)))
