import matplotlib.pyplot as plt
import numpy as np
import math
import scipy
import pandas as pd
from scipy import io
import glob
import os
import plotting


def read_egglaying(basepath,
                   filelist,
                   groupnames=[],
                   excel=False,
                   sheetname='virgin_egg_counts'


                   ):
    '''loads the specified files into one dataframe'''

    li = []
    if not groupnames:
        groupnames = filelist

    for (filename, groupname) in zip(filelist, groupnames):
        filepath = os.path.join(basepath, filename)
        if excel:
            df = pd.read_excel(filepath, sheetname)

        else:
            df = pd.read_csv(filepath, index_col=None, header=0)

        df["group"] = groupname
        li.append(df)

    dfs = pd.concat(li, axis=0, ignore_index=True)
    return dfs


def preprocess_egglaying(df, column1="24h", column2="48h"):
    '''calculates total eggs and drops NaNs'''
    df["tot"] = df[column1] + df[column2]
    removed_nans = df.dropna()
    return removed_nans


def egglayingplots(basepath,
                   filelist,
                   outputpath,
                   groupnames=[],
                   column1="24h",
                   column2="48h",
                   yaxlabel='eggs 24h',
                   yaxlabel2='eggs 48h',
                   colours=[['#bb44bb', '#d68ed6'],
                            ['#E3B6E3', '#F8EDF8'],
                            ['#823082', '#E4B5E4'],
                            ['#808080', '#b2b2b2']]):
    '''loads data and performs egglaying plots'''
    df = read_egglaying(basepath, filelist, groupnames=groupnames)
    df_preprocessed = preprocess_egglaying(
        df, column1=column1, column2=column2)
    outputpath24h = outputpath.replace('.eps', '_24h.eps')
    outputpath48h = outputpath24h.replace('24h', '48h')
    plotting.boxplot_groups(df_preprocessed,
                            'group',
                            column1,
                            outputpath24h,
                            yaxlabel=yaxlabel,
                            colours=colours,
                            sort=False)
    plotting.boxplot_groups(df_preprocessed,
                            'group',
                            'tot',
                            outputpath48h,
                            yaxlabel=yaxlabel2,
                            colours=colours,
                            sort=False)


def virgin_eggplots(basepath,
                    filelist,
                    outputpath,
                    groupnames=[],
                    yaxlabel='eggs 5 days',
                    colours=[['#bb44bb', '#d68ed6'],
                             ['#E3B6E3', '#F8EDF8'],
                             ['#823082', '#E4B5E4'],
                             ['#808080', '#b2b2b2']],
                    sheetname='virgin_egg_counts',
                    columname='group housed',
                    subsetcolumn='chamber id',
                    drop_duplicates=True):
    '''loads data and performs egglaying plots'''

    df = read_egglaying(basepath,
                        filelist,
                        groupnames=groupnames,
                        sheetname=sheetname,
                        excel=True
                        )
    if drop_duplicates:
        df = df.drop_duplicates(subset=subsetcolumn)

    df = df[df[columname].notna()]

    plotting.boxplot_groups(df, 'group',
                            columname,
                            outputpath,
                            yaxlabel=yaxlabel,
                            colours=colours,
                            sort=False)
