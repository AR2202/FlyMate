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
from lifelines import*
from lifelines.statistics import multivariate_logrank_test


def load_copulation(basepath, filename):
    '''loads the specified file and removes NaNs'''

    filepath = os.path.join(basepath, filename)
    df = pd.read_csv(filepath, header=None)
    removed_nan = df.dropna()
    observed = [False if data == "None" else True for data in removed_nan[0]]
    removed_nan[0][removed_nan[0] == 'None'] = 3600 * 25
    seconds = [int(frames)/25 for frames in removed_nan[0]]
    in10min = [600.0 if int(
        frames)/25 > 600.0 else int(frames)/25 for frames in removed_nan[0]]
    return seconds, in10min, observed


def kmf_copulation(seconds, in10min, observed, groupname):
    '''performs kaplan-Meier-fit'''
    kmf = KaplanMeierFitter(label=groupname)
    kmf.fit(seconds, event_observed=observed)
    kmf_10min = KaplanMeierFitter(label=groupname)
    kmf_10min.fit(in10min, event_observed=observed)
    return kmf, kmf_10min


def kmf_plot(basepath, filelist, outfilename, groupnames=[], colors=[['#bb44bb', '#d68ed6'], ['#808080', '#b2b2b2'], ['#808080', '#b2b2b2']], hour=True):
    '''loads the specified files and performs kaplan-Meier-fit and plot'''

    if not groupnames:
        groupnames = filelist
    outputpath = os.path.join(basepath, outfilename)
    group = 0
    timetocop = []
    groups = []
    observed_all = []
    fig, ax = plt.subplots()
    ax.set_xlabel('s')
    ax.set_ylabel('fraction copulated')

    for (filename, (groupname, color)) in zip(filelist, zip(groupnames, colors)):
        seconds, in10min, observed = load_copulation(basepath, filename)
        kmf, kmf_10min = kmf_copulation(seconds, in10min, observed, groupname)
        if hour:
            kmf.plot_cumulative_density(color=color)
            timetocop = timetocop + seconds
        else:
            kmf_10min.plot_cumulative_density(color=color)
            timetocop = timetocop + in10min
        observed_all = observed_all + observed
        groupvals = [group for data in observed]
        groups = groups + groupvals
        group += 1
    plt.savefig(outputpath)
    logrank_cop(timetocop, groups, observed_all)


def logrank_cop(timetocop, groups, observed):
    logranktest = multivariate_logrank_test(
        timetocop, groups, event_observed=observed)
    logranktest.test_statistic
    logranktest.p_value
    print(logranktest.summary)
