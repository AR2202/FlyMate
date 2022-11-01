import matplotlib.pyplot as plt
import numpy as np
import os
import math
import scipy
import indices
import pandas as pd
from scipy import io
import statsmodels.api as sm
import statsmodels.formula.api as smf
import lifelines
from lifelines import *
from lifelines.statistics import multivariate_logrank_test


def load_survival_data(basepath, filename, filetype='csv', behaviour='init'):
    '''loads the survival curve data from either the csv file for copulation or .mat file for initiation'''
    filepath = os.path.join(basepath, filename)
    if filetype == 'csv':

        df = pd.read_csv(filepath, header=None)
    elif filetype == 'mat':
        df_all = indices.load_indices_file(basepath, filename)
        df = df_all[behaviour]
    else:
        print("filetype {} not supported".format(filetype))
        return
    return df


def prepare_survival_data_copulation(df, in_frames=True, fps=25, xmin=10.0):
    '''calculates time and removes NaNs'''
    removed_nan = df.dropna()
    observed = [False if data == "None" else True for data in removed_nan[0]]

    xseconds = xmin * 60.0
    if in_frames:
        removed_nan[0][removed_nan[0] == 'None'] = 3600 * fps
        seconds = [int(frames)/fps for frames in removed_nan[0]]
        inxmin = [xseconds if int(
            frames)/fps > xseconds else int(frames)/fps for frames in removed_nan[0]]
    else:
        removed_nan[0][removed_nan[0] == 'None'] = 3600
        seconds = [int(sec) for sec in removed_nan[0]]
        inxmin = [xseconds if int(frames) > xseconds else int(
            frames) for frames in removed_nan[0]]

    return seconds, inxmin, observed


def prepare_survival_data_initiation(df, in_frames=False, fps=25, xmin=15.0):
    '''calculates time and removes NaNs'''
    init_first_removed = df.replace(0.04, 900)
    init_nan_removed = init_first_removed.replace(np.nan, 900)

    observed = [False if int(
        data) == 900 else True for data in init_nan_removed]

    xseconds = xmin * 60.0
    if in_frames:

        seconds = [int(frames)/fps for frames in init_nan_removed]
        inxmin = [xseconds if int(
            frames)/fps > xseconds else int(frames)/fps for frames in init_nan_removed]
    else:

        seconds = [int(sec) for sec in init_nan_removed]
        inxmin = [xseconds if int(secs) > xseconds else int(
            secs) for secs in init_nan_removed]

    return seconds, inxmin, observed


def load_copulation(basepath, filename, in_frames=True, fps=25, xmin=10.0):
    '''loads the specified file and removes NaNs'''
    df = load_survival_data(basepath, filename)
    seconds, inxmin, observed = prepare_survival_data_copulation(
        df, in_frames=in_frames, fps=fps, xmin=xmin)

    return seconds, inxmin, observed


def load_initiation(basepath, filename, in_frames=False, fps=25, xmin=15.0):
    '''loads the specified file and removes NaNs'''
    df = load_survival_data(basepath, filename, filetype='mat')
    seconds, inxmin, observed = prepare_survival_data_initiation(
        df, in_frames=in_frames, fps=fps, xmin=xmin)

    return seconds, inxmin, observed


def kmf_copulation(seconds,  inxmin, observed, groupname, in_min=True):
    '''performs kaplan-Meier-fit'''
    kmf = KaplanMeierFitter(label=groupname)
    kmf_xmin = KaplanMeierFitter(label=groupname)
    minutes = [s/60.0 for s in seconds]
    minutes_xmin = [s/60.0 for s in inxmin]
    if in_min:
        kmf.fit(minutes, event_observed=observed)
        kmf_xmin.fit(minutes_xmin, event_observed=observed)
    else:
        kmf.fit(seconds, event_observed=observed)
        kmf_xmin.fit(inxmin, event_observed=observed)

    return kmf, kmf_xmin


def kmf_plot(basepath, filelist, outfilename, groupnames=[],
             colors=[['#bb44bb', '#d68ed6'], [
                 '#808080', '#b2b2b2'], ['#808080', '#b2b2b2']],
             hour=True, xlabel='min', ylabel='fraction copulated',
             in_frames=True, fps=25, xmin=10.0, copulation=True, in_min=True):
    '''loads the specified files and performs kaplan-Meier-fit and plot'''

    if not groupnames:
        groupnames = filelist
    outputpath = os.path.join(basepath, outfilename)
    group = 0
    timetocop = []
    groups = []
    observed_all = []
    fig, ax = plt.subplots()

    ax.set_ylabel(ylabel)

    for (filename, (groupname, color)) in zip(filelist, zip(groupnames, colors)):
        if copulation:
            seconds, inxmin, observed = load_copulation(
                basepath, filename, in_frames=in_frames, fps=fps, xmin=xmin)
        else:
            seconds, inxmin, observed = load_initiation(
                basepath, filename, in_frames=in_frames, fps=fps, xmin=xmin)

        kmf, kmf_xmin = kmf_copulation(
            seconds, inxmin, observed, groupname, in_min=in_min)
        if hour:
            kmf.plot_cumulative_density(color=color)
            timetocop = timetocop + seconds
        else:
            kmf_xmin.plot_cumulative_density(color=color)
            timetocop = timetocop + inxmin
        observed_all = observed_all + observed
        groupvals = [group for data in observed]
        groups = groups + groupvals
        group += 1
    ax.set_xlabel(xlabel)
    plt.savefig(outputpath)
    logrank_cop(timetocop, groups, observed_all)


def logrank_cop(timetocop, groups, observed):
    logranktest = multivariate_logrank_test(
        timetocop, groups, event_observed=observed)
    logranktest.test_statistic
    logranktest.p_value
    print(logranktest.summary)
