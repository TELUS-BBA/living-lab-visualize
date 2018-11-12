#!/usr/bin/env python3

# Combines the pings from different dates in data/ping/
# and writes them to /home/ubuntu/data/ping.csv .

import os
import pandas as pd


def combine_pings(source_dir):
    _, _, file_list = list(os.walk(source_dir))[0]
    df = pd.read_csv(os.path.join(source_dir, file_list[0]))
    del file_list[0]
    for file_name in file_list:
        new_df = pd.read_csv(os.path.join(source_dir, file_name))
        df = df.append(new_df, ignore_index=True)
    df.loc[:, 'time'] = pd.to_datetime(df.loc[:, 'time'])
    df.loc[:, 'down'] = df.loc[:, 'down'].astype(int)
    df.loc[:, 'up'] = df.loc[:, 'up'].astype(int)
    df = df.set_index(['nanopi_id', 'time']).sort_index()
    return df


if __name__ == '__main__':

    source_dir = '/home/ubuntu/living-lab-visualize/data/ping/'
    dest_dir = '/home/ubuntu/data/'

    df = combine_pings(source_dir)

    df.to_csv(os.path.join(dest_dir, 'ping.csv'))
