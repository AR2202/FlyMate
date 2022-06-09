import matplotlib.pyplot as plt
import numpy as np
import math
import scipy
import pandas as pd
from scipy import io
import glob
import os
import plotting


def read_egglaying(basepath, filelist, groupnames=[]):
    '''loads the specified files into one dataframe'''

    li = []
    if not groupnames:
        groupnames = filelist

    for (filename, groupname) in zip(filelist, groupnames):
        filepath = os.path.join(basepath, filename)
        df = pd.read_csv(filepath, index_col=None, header=0)
        df["group"] = groupname
        li.append(df)

    dfs = pd.concat(li, axis=0, ignore_index=True)
    return dfs


def preprocess_egglaying(df, column1="24h", column2="48h"):
    '''calculated total eggs and drops NaNs'''
    df["tot"] = df[column1] + df[column2]
    removed_nans = df.dropna()
    return removed_nans


def egglayingplots(basepath, filelist, outputpath, groupnames=[], column1="24h", column2="48h", yaxlabel='eggs 24h', yaxlabel2='eggs 48h'):
    '''loads data and performs egglaying plots'''
    df = read_egglaying(basepath, filelist, groupnames=groupnames)
    df_preprocessed = preprocess_egglaying(
        df, column1=column1, column2=column2)
    plotting.boxplot_groups(df_preprocessed, 'group',
                            column1, outputpath, yaxlabel=yaxlabel)
    plotting.boxplot_groups(df_preprocessed, 'group',
                            'tot', outputpath, yaxlabel=yaxlabel2)
