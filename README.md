# living-lab-visualize

This repository contains code that produces graphs that help us interpret results obtained with living-lab.
It mainly uses pandas, a python data science library, to do this.
You can think of pandas as excel on steroids.
The main object from pandas is a "dataframe", which is equivalent to an excel spreadsheet:
it has indices, rows and columns.
Pandas lets us slice, dice, combine and process the data, and then plot it.


## Installation

Only Linux is supported, although you may have luck running the scripts on other platforms
if you install a Python data science distribution such as Anaconda.
You should also be on some version of Python 3 (it is confirmed to work on python 3.5.2).
To install on Linux:

    git clone https://github.com/adamkpickering/living-lab-visualize.git
    cd living-lab-visualize
    sudo pip3 install -r requirements.txt


## Usage

Before we get in depth, all you may be looking for is to generate a few plots
to get an idea of what the data looks like.
If that's the case, first establish an SSH local tunnel from the API to your machine.
Then, run:

    ./common.py
    ./plot.py

Plots will be produced in the current directory.
But you can get more out of this if you take some time to learn about it and understand it.
If that is the case, read on.

The typical workflow for creating plots is:

1.  Get data from API, and format it into a pandas dataframe
    - alternatively you may want to download the data and then work off of a local
      copy - more on this later
    - functions for this are located in `common.py`

1.  Filter it in some way to get the set of data you want to plot (optional)
    - you take care of this in whatever script you're using to create plots

1.  Pass the dataframe into a plotting function, which creates and saves the plot for you
    - get your plotting functions from `bandwidth.py`, `jitter.py`, `latency.py` and `ping.py`
      - each file is named according to the type of test it works with

This usage guide provides basic info, but you may find it lacking.
Ultimately there is no substitute for reading the pandas documentation and example code.


### Getting Data and Formatting it into Pandas Dataframes

You have two options when producing graphs:

1.  Pull the data from the API, format it into a dataframe, then produce plots from it.

1.  Pull the data from the API, format it into a dataframe, and save it into HDF5 format.
    Then, in a separate script open the HDF5 files and plot from those.

Option 1 is more convenient for small datasets.
However you may find that this takes too long for large data sets
or slow network connections - that is when you might consider option 2.
Option 2 is also good if you want to save a snapshot of the data as it
existed at a certain moment in time.

Either way, you must start by running functions in `common.py`.
Functions that get dataframes from the API are named `get_XX_dataframe(...)`,
where XX is one of bandwidth, jitter, latency, and ping.
Once you have the dataframe you may either proceed to the next step (filtering), or save it to HDF5.
See [this guide](https://pandas.pydata.org/pandas-docs/stable/io.html#io-hdf5)
for help with reading and writing pandas dataframes to and from HDF5.
You can reference (or even use outright) `plot.py` for examples.
There are also examples in the `if __name__ == '__main__'` sections
of `bandwidth.py`, `jitter.py`, `latency.py`, and `ping.py`.

#### URL Parameters
You may want to filter your API query with URL parameters.
If this is the case, simply browse to the API and click on "Filters",
which will let you learn about which URL parameters do what.

#### Changing Variables in common.py
You may have to change the values of the global variables `BASE_URL` and `TIMEZONE` in `common.py`.
`BASE_URL` is the base URL of the API, and `TIMEZONE` is the timezone that
the NanoPis were in for testing.


### Filtering Pandas Dataframes

When making plots you may want to filter or slice your dataframe in some way.
There are two ways I can think of that might be useful:

1.  **By NanoPi:** To filter your dataframe by NanoPi, run the following command:

        df1 = df.loc[(slice(None), [11, 12, 13], slice(None)), :]

    Where `[11, 12, 13]` is a list of NanoPi IDs that you want
    to remain in the new dataframe, and `df1` is the new dataframe.

1.  **By Date:** Limiting the dataframe by date is similar to the above.
    If we want to limit my dataframe to all the data between the dates 2018-05-30
    and 2018-05-31 we can use the command:

        df1 = df.loc[(slice('2018-05-30', '2018-05-31'), slice(None), slice(None)), :]

    We can get greater granularity. If we want the data from 2018-05-30 at 22:30:00
    to 2018-05-31 at 19:00:00 we can use the command:
    
        df1 = df.loc[(slice('2018-05-30 22:30:00', '2018-05-31 19:00:00'), slice(None), slice(None)), :]

It is impossible for me to anticipate all of your filtering needs.
If these pointers don't help, your best resource will be to learn about pandas.
A good place to start is [here](http://pandas.pydata.org/pandas-docs/stable/10min.html).
Remember: you are limited in the operations you may do on dataframes
if you want to use the plotting functions.
These functions expect the dataframe to have the same type of index,
and the same columns and column names as the ones originally produced by the
`get_XX_dataframe(...)` functions.


### Plot Types

Once you have the dataframe you want to plot, you can pass it to any of the plotting functions in 
`bandwidth.py`, `jitter.py`, `latency.py`, and `ping.py`.
I have included a summary of plot types here, but you can also
look at the function docstrings for explanations of what they do
and how to call them.

#### Average
Average plots are intended to show the average values of each NanoPi in the dataframe
over the entire time covered by the dataframe.

#### Hour of Day
Hour of Day plots are intended to show any relationships the data has to what time of day
it was collected. There are two types of Hour of Day plots: **individual** and **aggregate**.
Individual plots plot the data for each NanoPi in the dataframe 
as a separate series so that you can compare the data collected by different NanoPis.
Aggregate plots plot the average of all the NanoPis in the passed dataframe,
so that you can aggregate data from multiple NanoPis into a single series.

#### Day of Week
Day of Week plots are equivalent to Hour of Day plots,
except that they are meant to show relationships between collected data and
the day of the week that data was collected on.
Once again, there are two types of Day of Week plots: **individual** and **aggregate**.
The same explanations apply.

#### Coverage
Coverage plots are a visual representation of which data points are present and which are missing.
If data is missing, it shows up as a black patch; white patches represent data that is present.
You might use coverage plots to get an idea of the quality of your data set,
or to see if there are any bugs that are causing tests to be missed.
