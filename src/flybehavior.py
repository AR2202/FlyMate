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
    """read in excel file of behaviour data and make individual csv files for 
    egglaying and time to copulation"""

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


def write_indices_csv_files(basefilenames, basepath_behaviour_analyisis,
                            outputpath, outfilename, other=False):
    """read .mat file of behaviour data and make indices csv files"""

    if other:
        matfilenames = [basefilename +
                        '_Indices_other.mat' for basefilename in basefilenames]
        outputfile = os.path.join(
            outputpath, outfilename + '_Indices_other.csv')
    else:
        matfilenames = [basefilename +
                        '_Indices.mat' for basefilename in basefilenames]
        outputfile = os.path.join(outputpath, outfilename + '_Indices.csv')

    dfs = indices.load_indices_files(
        basepath_behaviour_analyisis, matfilenames)
    dfs.to_csv(outputfile, index=False)


def female_behaviour(basefilenames, basepath_tracking, basepath_behaviour,
                     outfilename,
                     groupnames=[],
                     yaxlabels_behaviour=[],
                     colours=[['#bb44bb', '#d68ed6'], [
                         '#404040', '#737373'], ['#808080', '#b2b2b2']],
                     hour=True,
                     ylim=(-0.1, 1),
                     include_virgin_egglaying=True,
                     sheetname_virgin_egglaying='virgin_egg_counts',
                     columname_virgin_egg_counts='group housed'):
    '''analyses files of standard female behaviour data'''
    excelfilenames = [basefilename +
                      '.xlsx' for basefilename in basefilenames]
    eggfilenames = [basefilename +
                    '_egglaying.csv' for basefilename in basefilenames]
    eggplotname = outfilename + '_egglaying.eps'
    eggplotname_virgin = outfilename + '_egglaying_virgin.eps'
    timetocopfilenames = [basefilename +
                          '_timetocop.csv' for basefilename in basefilenames]
    timetocopplot = outfilename + '_timetocopulation.eps'
    indices_other_filenames = [
        basefilename + '_Indices_other.mat' for basefilename in basefilenames]
    pausingfilenames = [
        basefilename + '_pausing_mean_fraction_frames.mat'
        for basefilename in basefilenames]
    distfilenames = [basefilename +
                     '_mean_dist.mat' for basefilename in basefilenames]
    distanceplot = outfilename + '_distance_travelled.eps'
    distancepath = os.path.join(basepath_tracking, distanceplot)
    velfilenames = [basefilename +
                    '_mean_velocity.mat' for basefilename in basefilenames]
    velocityplot = outfilename + '_velocity.eps'
    velpath = os.path.join(basepath_tracking, velocityplot)

    pausingplot = outfilename + '_pausing.eps'
    outputpath_pausing = os.path.join(basepath_tracking, pausingplot)
    outputpath_egglaying = os.path.join(basepath_behaviour, eggplotname)
    outputpath_timetocop = os.path.join(basepath_behaviour, timetocopplot)
    outputpath_virgin_egglaying = os.path.join(
        basepath_behaviour, eggplotname_virgin)
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
    except Exception as e:
        print("unable to do time to copulation analysis")
        print(e)

    '''egglaying'''
    try:
        egglaying.egglayingplots(basepath_behaviour,
                                 eggfilenames,
                                 outputpath_egglaying,
                                 groupnames=groupnames,
                                 colours=colours)
    except FileNotFoundError:
        print("unable to perform egglaying analysis: csv file of egg counts not found")
    except Exception as e:
        print("unable to do egglaying analysis")
        print(e)

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
    except Exception as e:
        print("unable to do pausing analysis")
        print(e)

    '''indices of male towards female'''
    try:
        indices_df = indices.load_indices_files(basepath_tracking,
                                                indices_other_filenames,
                                                groupnames=groupnames)
        indices.plot_indices(indices_df, basepath_tracking, outfilename,
                             yaxlabels=yaxlabels_behaviour, colours=colours, ylim=ylim)
    except FileNotFoundError:
        print("unable to do indices analysis: no such file")
    except IndexError:
        print("unable to perform index analysis: the file appears to be empty")
    except Exception as e:
        print("unable to do indices analysis")
        print(e)

    '''distance travelled'''
    try:
        dist = distancetravelled.load_dist_files(
            basepath_tracking, distfilenames)
        distancetravelled.plot_dist(dist, distancepath, colours=colours)
    except FileNotFoundError:
        print("unable to do distance travelled analysis: no such file")
    except IndexError:
        print("unable to perform distance travelled analysis: the file appears to be empty")
    except Exception as e:
        print(e)

    '''velocity'''
    try:
        vel = distancetravelled.load_dist_files(
            basepath_tracking, velfilenames)
        distancetravelled.plot_dist(vel, velpath,
                                    colours=colours,
                                    ylim=(0, 10),
                                    yaxlabel='velocity')
    except FileNotFoundError:
        print("unable to do velocity analysis: no such file")
    except IndexError:
        print("unable to perform valocity analysis: the file appears to be empty")
    except Exception as e:
        print(e)

        '''virgin egglaying'''
    if include_virgin_egglaying:
        try:
            egglaying.virgin_eggplots(basepath_behaviour,
                                      excelfilenames,
                                      outputpath_virgin_egglaying,
                                      groupnames=groupnames,
                                      colours=colours,
                                      columname=columname_virgin_egg_counts,
                                      sheetname=sheetname_virgin_egglaying)
        except FileNotFoundError:
            print("unable to do virgin egglaying analysis: excelfile not found")
        except Exception as e:
            print(e)


def male_behaviour(basefilenames, basepath_tracking, basepath_behaviour,
                   outfilename,
                   groupnames=[],
                   yaxlabels_behaviour=[],
                   colours=[['#bb44bb', '#d68ed6'], [
                       '#404040', '#737373'], ['#808080', '#b2b2b2']],
                   hour=True,
                   ylim=(-0.1, 1)):
    '''analyses files of standard male behaviour data'''

    timetocopfilenames = [basefilename +
                          '_timetocop.csv' for basefilename in basefilenames]
    timetocopplot = outfilename + '_timetocopulation.eps'
    indices_filenames = [
        basefilename + '_Indices.mat' for basefilename in basefilenames]

    outputpath_timetocop = os.path.join(basepath_behaviour, timetocopplot)
    distfilenames = [basefilename +
                     '_mean_dist_other.mat' for basefilename in basefilenames]

    distanceplot = outfilename + '_distance_travelled.eps'
    distancepath = os.path.join(basepath_tracking, distanceplot)
    disttootherfilenames = [basefilename +
                            '_mean_distance_to_other.mat' for basefilename in basefilenames]

    disttootherplot = outfilename + '_distance_to_other.eps'
    disttootherpath = os.path.join(basepath_tracking, disttootherplot)
    velfilenames = [basefilename +
                    '_mean_velocity.mat' for basefilename in basefilenames]
    velocityplot = outfilename + '_velocity.eps'
    velpath = os.path.join(basepath_tracking, velocityplot)
    bilateralfilenames = [basefilename +
                          '_bilateral_WingIndex.mat' for basefilename in basefilenames]
    bilatplot = outfilename + '_bilateral_wing_extension.eps'
    bilatpath = os.path.join(basepath_tracking, bilatplot)
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
    except Exception as e:
        print(e)

    '''indices of male towards female'''
    try:
        indices_df = indices.load_indices_files(basepath_tracking,
                                                indices_filenames,
                                                groupnames=groupnames)
        indices.plot_indices(indices_df, basepath_tracking, outfilename,
                             yaxlabels=yaxlabels_behaviour, colours=colours,
                             ylim=ylim)
    except FileNotFoundError:
        print("unable to do indices analysis: no such file")
    except IndexError:
        print("unable to perform index analysis: the file is empty")
    except Exception as e:
        print(e)

    '''velocity'''
    try:
        vel = distancetravelled.load_dist_files(
            basepath_tracking, velfilenames)
        distancetravelled.plot_dist(vel, velpath,
                                    colours=colours,
                                    ylim=(0, 10),
                                    yaxlabel='velocity')
    except FileNotFoundError:
        print("unable to do velocity analysis: no such file")
    except IndexError:
        print("unable to perform velocity analysis: the file appears to be empty")
    except Exception as e:
        print(e)

    '''distance to other'''
    try:
        disttoother = distancetravelled.load_dist_files(
            basepath_tracking, disttootherfilenames)
        distancetravelled.plot_dist(disttoother, disttootherpath,
                                    colours=colours,
                                    ylim=(0, 20),
                                    yaxlabel='distance to other')
    except FileNotFoundError:
        print("unable to do distance to other analysis: no such file")
    except IndexError:
        print("unable to perform distance to other analysis: the file appears to be empty")
    except Exception as e:
        print(e)

    '''distance travelled of female paired with this male'''

    try:
        dist = distancetravelled.load_dist_files(
            basepath_tracking, distfilenames)

        distancetravelled.plot_dist(
            dist, distancepath, yaxlabel='distance travelled female', colours=colours)
    except FileNotFoundError:
        print("unable to do distance travelled analysis: no such file")
    except IndexError:
        print("unable to perform distance travelled analysis: the file appears to be empty")
    except Exception as e:
        print(e)

    '''bilateral wing extension'''
    try:
        bilat = bilateral.load_bilateral_files(
            basepath_tracking, bilateralfilenames)

        bilateral.plot_bilateral(
            bilat, bilatpath, yaxlabel='bilateral wing extension',
            colours=colours,
            ylim=ylim)
    except FileNotFoundError:
        print("unable to do bilateral wing extension analysis: no such file")
    except IndexError:
        print("unable to perform bilateral wing extension analysis: the file appears to be empty")
    except Exception as e:
        print(e)
