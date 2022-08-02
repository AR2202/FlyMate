from turtle import color
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import io
import os
import plotting


def load_fraction_file(basepath, filename):
    '''loads the .mat files of fraction of frames 
    positive for the given behaviour 
    and returns a pandas DataFrame of the data'''
    filepath = os.path.join(basepath, filename)
    filecontents = io.loadmat(filepath)
    df = pd.DataFrame(filecontents['frac'][0])
    return df


def load_fraction_files(basepath, filelist, groupnames=[]):
    '''loads several files into one dataframe in long format'''

    li = []
    if not groupnames:
        groupnames = filelist

    for (filename, groupname) in zip(filelist, groupnames):
        df = load_fraction_file(basepath, filename)
        df["group"] = groupname
        li.append(df)

    dfs = pd.concat(li, axis=0, ignore_index=True)
    return dfs


def plot_frac(df, outputpath, group='group', yaxlabel='fraction', ylim=(0, 1), colours=[['#bb44bb', '#d68ed6'], [
        '#E3B6E3', '#F8EDF8'], ['#823082', '#E4B5E4'], ['#808080', '#b2b2b2']]):
    plotting.boxplot_groups(df, group, 0, outputpath,
                            yaxlabel=yaxlabel, ylim=ylim, colours=colours)


def plot_pausing(df, outputpath, group='group', yaxlabel='fraction pausing', ylim=(0, 1), colours=[['#bb44bb', '#d68ed6'], [
        '#E3B6E3', '#F8EDF8'], ['#823082', '#E4B5E4'], ['#808080', '#b2b2b2']]):
    plotting.boxplot_groups(df, group, 0, outputpath,
                            yaxlabel=yaxlabel, ylim=ylim, colours=colours)
