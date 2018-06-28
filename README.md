# living-lab-visualize

This repository contains code that produces graphs that help us interpret results obtained with living-lab.
It mainly uses pandas, a python data science library, to do this.
You can think of pandas as excel on steroids.
The main object from pandas is a "dataframe", which is equivalent to an excel spreadsheet:
it has indices, rows and columns.
Pandas lets us slice, dice, combine and process the data, and then output it to plots.


## Summary

The typical workflow for creating plots is:

1.  Get data from API, and put it into a pandas dataframe
    - alternatively you may want to download the data and then work off of a local
      copy - more on this later
    - functions for this are located in `common.py`

1.  Filter it in some way to get the set of data you want to plot (optional)
    - you take care of this in whatever script you're using to create plots

1.  Pass the dataframe into a plotting function, which creates and saves the plot for you
    - get your plotting functions from `bandwidth.py`, `jitter.py`, `latency.py` and `ping.py`
      - each file is named according to the type of test it works with


## Installation

To be completed.


## Usage

- how to select specific (groups of) nanopis
- how to select by time frame
- about geting data into local HDF5 format (for slow connections, or for snapshots)


## Plot Types

### Average
Average plots are intended to show the average values of each NanoPi in the passed dataframe
over the entire time covered by the dataframe.

### Hour of Day
Hour of Day plots are intended to show any relationships the data has to what time of day
it was collected. There are two types of Hour of Day plots: **individual** and **aggregate**.
Individual plots plot the data for each NanoPi in the passed dataframe 
as a separate series so that you can compare the data collected by different NanoPis.
Aggregate plots plot the average of all the NanoPis in the passed dataframe,
so that you can aggregate data from multiple NanoPis into a single series.

### Day of Week
Day of Week plots are equivalent to Hour of Day plots,
except that they are meant to show relationships between collected data and
the day of the week that data was collected on.
Once again, there are two types of Day of Week plots: **individual** and **aggregate**.

### Coverage
Coverage plots help you visualize missing data.
If data was missing, that shows up as a black patch;
white patches represent data that was present.
You might use coverage plots to get an idea of the quality of your data set,
or to see if there are any bugs that are causing tests to be missed.
