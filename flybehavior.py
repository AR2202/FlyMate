import pandas as pd
import os
from scipy import io
import egglaying
import timetocop
import indices
import fraction
import rpy2


def female_behaviour(basefilenames, basepath_tracking, basepath_behaviour, outfilename,
                     groupnames=[],
                     yaxlabels_behaviour=[],
                     colours=[['#bb44bb', '#d68ed6'], [
                         '#808080', '#b2b2b2'], ['#808080', '#b2b2b2']],
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
    pausingplot = outfilename + '_pausing.eps'
    outputpath_pausing = os.path.join(basepath_tracking, pausingplot)
    outputpath_egglaying = os.path.join(basepath_behaviour, eggplotname)
    outputpath_timetocop = os.path.join(basepath_behaviour, timetocopplot)
    ''' time to copulation'''
    timetocop.kmf_plot(basepath_behaviour,
                       timetocopfilenames,
                       outputpath_timetocop,
                       groupnames=groupnames,
                       colors=colours,
                       hour=True)

    '''egglaying'''
    egglaying.egglayingplots(basepath_behaviour,
                             eggfilenames,
                             outputpath_egglaying,
                             groupnames=groupnames)
    '''pausing'''
    pausing_df = fraction.load_fraction_files(basepath_tracking,
                                              pausingfilenames,
                                              groupnames=groupnames)
    fraction.plot_pausing(pausing_df, outputpath_pausing)
    '''indices of male towards female'''
    indices_df = indices.load_indices_files(basepath_tracking,
                                            indices_other_filenames,
                                            groupnames=groupnames)
    indices.plot_indices(indices_df, basepath_tracking, outfilename,
                         yaxlabels=yaxlabels_behaviour)

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
    ''' time to copulation'''
    timetocop.kmf_plot(basepath_behaviour,
                       timetocopfilenames,
                       outputpath_timetocop,
                       groupnames=groupnames,
                       colors=colours,
                       hour=True)

    
    '''indices of male towards female'''
    indices_df = indices.load_indices_files(basepath_tracking,
                                            indices_filenames,
                                            groupnames=groupnames)
    indices.plot_indices(indices_df, basepath_tracking, outfilename,
                         yaxlabels=yaxlabels_behaviour)