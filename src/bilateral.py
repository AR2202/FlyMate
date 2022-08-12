import matplotlib.pyplot as plt
import numpy as np
import math
import scipy
import pandas as pd
from scipy import io
import glob
import os
import plotting


def load_bilateral_file(basepath, filename):
    '''loads the .mat files of distance travalled
    and returns a pandas DataFrame of the data'''
    filepath = os.path.join(basepath, filename)
    filecontents = io.loadmat(filepath)
    df = pd.DataFrame(filecontents['data'][0])
    return df


def load_bilateral_files(basepath, filelist, groupnames=[]):
    '''loads several files into one dataframe in long format'''

    li = []
    if not groupnames:
        groupnames = filelist

    for (filename, groupname) in zip(filelist, groupnames):
        df = load_bilateral_file(basepath, filename)
        df["group"] = groupname
        li.append(df)

    dfs = pd.concat(li, axis=0, ignore_index=True)
    return dfs


def plot_bilateral(df, outputpath, group='group', yaxlabel='bilateral wing index', ylim=(0, 1)):
    plotting.boxplot_groups(df, group, 0, outputpath,
                            yaxlabel=yaxlabel, ylim=ylim)
