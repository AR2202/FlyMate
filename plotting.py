import matplotlib.pyplot as plt
import numpy as np
import math
import scipy
import pandas as pd
from scipy import io
import glob
import os

def boxplots(data, colors, colors2, labels, yaxlabel, outputpath):
    '''This function plots the data in the given colours and with the provided labels
    saving the figure tho outputpath'''

    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(9, 6))
    bplot1 = plt.boxplot(data, vert=True, patch_artist=True)

    axes.tick_params(axis='both', direction='out')
    axes.yaxis.set_ticks_position('left')
    axes.xaxis.set_ticks_position('bottom')
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.spines['bottom'].set_visible(False)
    for axis in ['bottom', 'left']:
        axes.spines[axis].set_linewidth(2)

    axes.xaxis.set_tick_params(width=0)
    axes.yaxis.set_tick_params(width=2)
    plt.ylim(-1, 150)

    for patch, color in zip(bplot1['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_color(color)

    plt.xlabel('', fontsize=18)
    plt.ylabel(yaxlabel, fontsize=22)
    plt.tick_params(axis='both', labelsize=13)
    # change color and linewidth of the whiskers
    for whisker, color in zip(bplot1['whiskers'], colors2):
        whisker.set(color=color, linewidth=2, linestyle='-')

    # change color and linewidth of the caps
    for cap, color in zip(bplot1['caps'], colors2):
        cap.set(color=color, linewidth=2, linestyle='-')
    # change color and linewidth of the caps
    for flier, color in zip(bplot1['fliers'], colors2):
        flier.set(color=color, marker='o')

    plt.setp(bplot1['medians'], color='white', marker='', linewidth=2)
    plt.setp(axes, xticklabels=labels)
    plt.savefig(outputpath)

def boxplot_groups(df, groupby, datacolumn, yaxlabel='eggs 24h', ylim=(-1, 150),
                   boxprops=dict(linestyle='-', linewidth=4, color='k'),
                   medianprops=dict(linestyle='-', linewidth=4, color='k')):
    '''plots the dataframe by groups'''
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(9, 6))
    bplot1 = df.groupby(by=groupby).boxplot(column=datacolumn,
                                            subplots=False,
                                            vert=True,
                                            patch_artist=True,
                                            showmeans=True,
                                            boxprops=boxprops,
                                            medianprops=medianprops,
                                            return_type='both')
    axes.tick_params(axis='y', direction='out')
    axes.tick_params(axis='x', direction='out', labelsize= 0)
    axes.yaxis.set_ticks_position('left')
    axes.set_ylim(ylim)
    axes.set_xlabel("")
    axes.set_xticklabels([])
    axes.xaxis.set_ticks_position('bottom')
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.spines['bottom'].set_visible(False)
    for axis in ['bottom', 'left']:
        axes.spines[axis].set_linewidth(2)

    plt.ylim(ylim)
    plt.ylabel(yaxlabel, fontsize=22)
    plt.xlabel("")
    plt.tick_params(axis='both', labelsize=13)