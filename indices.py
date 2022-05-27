import matplotlib.pyplot as plt
import numpy as np
import math
import scipy
import pandas as pd
from scipy import io
import glob
import os
import plotting


def load_indices_file(basepath, filename):
    '''loads the .mat files of behavioural indices and returns a pandas DataFrame of the data'''
    filepath = os.path.join(basepath, filename)
    filecontents = io.loadmat(filepath)
    df = pd.DataFrame()
    for behaviour in filecontents['data'].dtype.names:
        if filecontents['data'][behaviour][0][0].size > 0:
            df[behaviour] = filecontents['data'][behaviour][0][0][0]
    return df


def load_indices_files(basepath, filelist, groupnames=[]):
    '''loads several files into one dataframe in long format'''

    li = []
    if not groupnames:
        groupnames = filelist

    for (filename, groupname) in zip(filelist, groupnames):
        df = load_indices_file(basepath, filename)
        df["group"] = groupname
        li.append(df)

    dfs = pd.concat(li, axis=0, ignore_index=True)
    return dfs


def plot_indices(df, group='group', yaxlabels=[], ylim=(-1, 100)):
    data = df.drop(columns=['group'])
    if not yaxlabels:
        yaxlabels = data.columns
    for (behaviour, yaxlabel) in zip(data.columns, yaxlabels):
        plotting.boxplot_groups(df, group, behaviour, yaxlabel=yaxlabel, ylim=ylim)