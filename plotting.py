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


def boxplot_groups(df, groupby, datacolumn, outputpath, yaxlabel='eggs 24h', ylim=(-1, 150),
                   boxprops=dict(linestyle='-', linewidth=1, color='k'),
                   medianprops=dict(linestyle='-', linewidth=1, color='white'),
                   meanprops={"marker": "s", "markerfacecolor": "white",
                              "markeredgecolor": "white"},
                   whiskerprops=dict(
                       linestyle='-', linewidth=1.0, color='gray'),
                   colours=[['#bb44bb', '#d68ed6'], [
                       '#E3B6E3', '#F8EDF8'], ['#823082', '#E4B5E4'], ['#808080', '#b2b2b2']]):
    '''plots the dataframe by groups'''

    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(9, 6))
    ax, bplot1 = df.groupby(by=groupby).boxplot(column=datacolumn,
                                                subplots=False,
                                                vert=True,
                                                patch_artist=True,

                                                showmeans=True,
                                                boxprops=boxprops,
                                                medianprops=medianprops,
                                                meanprops=meanprops,
                                                whiskerprops=whiskerprops,


                                                return_type='both')
    axes.tick_params(axis='y', direction='out')
    axes.tick_params(axis='x', direction='out', labelsize=0)
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
    for box, colourset in zip(bplot1['boxes'], colours):
        box.set_color(colourset[0])
        box.set_facecolor(colourset[1])

    plt.ylim(ylim)
    plt.ylabel(yaxlabel, fontsize=22)
    plt.xlabel("")
    plt.tick_params(axis='both', labelsize=13)

    plt.savefig(outputpath)
