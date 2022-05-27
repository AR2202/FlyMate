import matplotlib.pyplot as plt
import numpy as np
import math
import scipy
import pandas as pd
from scipy import io
import glob
import os





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

