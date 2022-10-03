import matplotlib.pyplot as plt
import numpy as np
import os
import math
import scipy
import pandas as pd
from scipy import io
import statsmodels.api as sm
import statsmodels.formula.api as smf
import lifelines
from lifelines import *
from lifelines.statistics import multivariate_logrank_test


def load_copulation(basepath, filename, in_frames=True, fps=25, xmin=10.0):
    '''loads the specified file and removes NaNs'''

    filepath = os.path.join(basepath, filename)
    df = pd.read_csv(filepath, header=None)
    removed_nan = df.dropna()
    observed = [False if data == "None" else True for data in removed_nan[0]]
    removed_nan[0][removed_nan[0] == 'None'] = 3600 * fps
    xseconds = xmin * 60.0
    if in_frames:
        seconds = [int(frames)/fps for frames in removed_nan[0]]
        inxmin = [xseconds if int(
            frames)/fps > xseconds else int(frames)/fps for frames in removed_nan[0]]
    else:
        seconds = [int(sec) for sec in removed_nan[0]]
        inxmin = [xseconds if int(frames) > xseconds else int(
            frames) for frames in removed_nan[0]]

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
             hour=True, xlabel='min', in_frames=True, fps=25, xmin=10.0):
    '''loads the specified files and performs kaplan-Meier-fit and plot'''

    if not groupnames:
        groupnames = filelist
    outputpath = os.path.join(basepath, outfilename)
    group = 0
    timetocop = []
    groups = []
    observed_all = []
    fig, ax = plt.subplots()

    ax.set_ylabel('fraction copulated')

    for (filename, (groupname, color)) in zip(filelist, zip(groupnames, colors)):
        seconds, inxmin, observed = load_copulation(
            basepath, filename, in_frames=in_frames, fps=fps, xmin=xmin)
        kmf, kmf_xmin = kmf_copulation(seconds, inxmin, observed, groupname)
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
