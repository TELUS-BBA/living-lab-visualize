# living-lab-visualize

Contains code that produces graphs that help us interpret results obtained with living-lab.

## Installation

## Usage

Of the four files `bandwidth.py`, `jitter.py`, `latency.py`, and `ping.py`,
each contains functions that produce plots related to the name of the file.
So `bandwidth.py` creates plots related to bandwidth, `jitter.py` creates plots related to jitter, etc.

`common.py` contains functions related to data fetching and processing.

The typical workflow for creating plots is:

1.  Get data from API, and put it into a pandas dataframe
      - use functions from `common.py` for this, such as `get_bandwidth_dataframe()`,
        `get_jitter_dataframe()`, etc.

1.  Filter it in some way to get the set of data you want to plot
      - use pandas dataframe methods for this

1.  Pass the filtered dataframe into a plotting function, which creates and saves the plot for you
      - get your plotting functions from `bandwidth.py`, `jitter.py`, `latency.py` and `ping.py`

- table depicting types of plots
- how to select specific (groups of) nanopis
- how to select by time frame
- about geting data into local HDF5 format (for slow connections, or for snapshots)
