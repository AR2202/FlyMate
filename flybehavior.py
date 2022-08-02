import pandas as pd
import os
from scipy import io
import egglaying
import timetocop
import indices
import fraction
import distancetravelled
import bilateral
import rpy2


def write_csv_files(basefilenames, basepath_behaviour):
    """read in excel file of behaviour data and make individual csv files for egglaying and time to copulation"""

    for basefile in basefilenames:
        excelfile = basefile + '.xlsx'
        filepath = os.path.join(basepath_behaviour, excelfile)
        timetocopfilename = basefile + '_timetocop.csv'
        eggfilename = basefile + '_egglaying.csv'
        df = pd.read_excel(filepath, header=None)
        timetocopulation = df[3]
        eggs24h = df[6]
        eggs48h = df[7]
        eggtable = pd.concat(
            (eggs24h.rename('24h'), eggs48h.rename('48h')), axis=1)

        outputpath_timetocop = os.path.join(
            basepath_behaviour, timetocopfilename)
        timetocopulation.to_csv(outputpath_timetocop,
                                index=False, header=False)
        outputpath_egglaying = os.path.join(basepath_behaviour, eggfilename)
        eggtable.to_csv(outputpath_egglaying, index=False)


def female_behaviour(basefilenames, basepath_tracking, basepath_behaviour, outfilename,
                     groupnames=[],
                     yaxlabels_behaviour=[],
                     colours=[['#bb44bb', '#d68ed6'], [
                         '#E3B6E3', '#F8EDF8'], ['#823082', '#E4B5E4'], ['#808080', '#b2b2b2']],
                     hour=True):
    '''analyses files of standard female behaviour data'''
    eggfilenames = [basefilename +
                    '_egglaying.csv' for basefilename in basefilenames]
    eggplotname = outfilename + '_egglaying.eps'
    timetocopfilenames = [basefilename +
                          '_timetocop.csv' for basefilename in basefilenames]
    timetocopplot = outfilename + '_timetocopulation.eps'
    indices_other_filenames = [
        basefilename + '_Indices_other.mat' for basefilename in basefilenames]
    pausingfilenames = [
        basefilename + '_pausing_mean_fraction_frames.mat' for basefilename in basefilenames]
    distfilenames = [basefilename +
                     '_mean_dist.mat' for basefilename in basefilenames]
    distanceplot = outfilename + '_distance_travelled.eps'

    pausingplot = outfilename + '_pausing.eps'
    outputpath_pausing = os.path.join(basepath_tracking, pausingplot)
    outputpath_egglaying = os.path.join(basepath_behaviour, eggplotname)
    outputpath_timetocop = os.path.join(basepath_behaviour, timetocopplot)
    ''' time to copulation'''
    try:
        timetocop.kmf_plot(basepath_behaviour,
                           timetocopfilenames,
                           outputpath_timetocop,
                           groupnames=groupnames,
                           colors=colours,
                           hour=hour)
    except FileNotFoundError:
        print("unable to do time to copulation analysis: no such file")

    '''egglaying'''
    try:
        egglaying.egglayingplots(basepath_behaviour,
                                 eggfilenames,
                                 outputpath_egglaying,
                                 groupnames=groupnames,
                                 colours=colours)
    except FileNotFoundError:
        print("unable to do  egglaying analysis")
    '''pausing'''
    try:
        pausing_df = fraction.load_fraction_files(basepath_tracking,
                                                  pausingfilenames,
                                                  groupnames=groupnames)
        fraction.plot_pausing(pausing_df, outputpath_pausing, colours=colours)
    except FileNotFoundError:
        print("unable to do pausing analysis")
    except IndexError:
        print("unable to perform pausing analysis: the file appears to be empty")

    '''indices of male towards female'''
    try:
        indices_df = indices.load_indices_files(basepath_tracking,
                                                indices_other_filenames,
                                                groupnames=groupnames)
        indices.plot_indices(indices_df, basepath_tracking, outfilename,
                             yaxlabels=yaxlabels_behaviour, colours=colours)
    except FileNotFoundError:
        print("unable to do indices analysis: no such file")
    except IndexError:
        print("unable to perform index analysis: the file appears to be empty")

    '''distance travelled'''
    try:
        dist = distancetravelled.load_dist_files(
            basepath_tracking, distfilenames)
        distancetravelled.plot_dist(dist, distanceplot, colours=colours)
    except FileNotFoundError:
        print("unable to do distance travelled analysis: no such file")
    except IndexError:
        print("unable to perform distance travelled analysis: the file appears to be empty")


def male_behaviour(basefilenames, basepath_tracking, basepath_behaviour, outfilename,
                   groupnames=[],
                   yaxlabels_behaviour=[],
                   colours=[['#bb44bb', '#d68ed6'], [
                       '#808080', '#b2b2b2'], ['#808080', '#b2b2b2']],
                   hour=True):
    '''analyses files of standard male behaviour data'''

    timetocopfilenames = [basefilename +
                          '_timetocop.csv' for basefilename in basefilenames]
    timetocopplot = outfilename + '_timetocopulation.eps'
    indices_filenames = [
        basefilename + '_Indices.mat' for basefilename in basefilenames]

    outputpath_timetocop = os.path.join(basepath_behaviour, timetocopplot)
    distfilenames = [basefilename +
                     '_mean_dist_other.mat' for basefilename in basefilenames]
    bilateralfilenames = [basefilename +
                          '_bilateral_WingIndex.mat' for basefilename in basefilenames]

    distanceplot = outfilename + '_distance_travelled.eps'
    ''' time to copulation'''
    try:
        timetocop.kmf_plot(basepath_behaviour,
                           timetocopfilenames,
                           outputpath_timetocop,
                           groupnames=groupnames,
                           colors=colours,
                           hour=hour)
    except FileNotFoundError:
        print("unable to do time to copulation analysis: no such file")

    '''indices of male towards female'''
    try:
        indices_df = indices.load_indices_files(basepath_tracking,
                                                indices_filenames,
                                                groupnames=groupnames)
        indices.plot_indices(indices_df, basepath_tracking, outfilename,
                             yaxlabels=yaxlabels_behaviour, colours=colours)
    except FileNotFoundError:
        print("unable to do indices analysis: no such file")
    except IndexError:
        print("unable to perform index analysis: the file is empty")
        '''distance travelled of female paired with this male'''
    try:
        dist = distancetravelled.load_dist_files(
            basepath_tracking, distfilenames)

        distancetravelled.plot_dist(
            dist, distanceplot, yaxlabel='distance travelled female', colours=colours)
    except FileNotFoundError:
        print("unable to do distance travelled analysis: no such file")
    except IndexError:
        print("unable to perform distance travelled analysis: the file appears to be empty")

    '''bilateral wing extension'''
    try:
        bilat = bilateral.load_bilateral_file(
            basepath_tracking, bilateralfilenames)

        bilateral.plot_bilateral(
            bilat, distanceplot, yaxlabel='distance travelled female', colours=colours)
    except FileNotFoundError:
        print("unable to do distance travelled analysis: no such file")
    except IndexError:
        print("unable to perform distance travelled analysis: the file appears to be empty")
