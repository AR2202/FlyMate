# FlyMate
Fly mating behaviour analysis scripts

<a name="top"></a>

# User Guide
Recommended Workflow:

* Track videos with goodwin-lab-tracking
* prepare data with AnnikasTrackingScripts
* Analyse data with the high-level modules outlined below
* usage of internal functions in other modules not recommended

## Modules
[Flybehaviour](#flybehaviour)

[Behaviourstats](#flybehaviour)

<a name="flybehavior"></a>
## Flybehaviour

The flybehaviour module is the top-level module and contains the functions
that should be used for analyis of tracking data. Import into jupyter notebook. Python required.

[write_csv_files](#write_csv_files)

[write_indices_csv_files](#write_indices_csv_files)

[female_behaviour](#female_behaviour)

[male_behaviour](#male_behaviour)

[Back to top](#top)

<a name="write_csv_files"></a>
`write_csv_files(basefilenames, basepath_behaviour)`

Function to write csv files of egglaying and time to copulation from excel file

### Parameters:

basefilenames: list of excel filenames(excluding '.xlsx' file extension)

basepath_behaviour: path to excel file

### Output:

None

Writes csv files to basepath_behaviour

[Back to top](#top)

[Up](#flybehavior)


<a name="write_indices_csv_files"></a>
`write_indices_csv_files(basefilenames, basepath_behaviour_analyisis,
                            outputpath, outfilename, other=False)`

Function to write csv files of indices file

### Parameters:

basefilenames: list of .mat filenames(excluding '.mat' file extension)

basepath_behaviour_analysis: path to .mat files

outputpath: path where csv file should be saved

outfilename: name for csv file

### Optional Keyword Arguments

other: Bool; if behaviour of the other fly in the chamber should be analysed (default False)

### Output:

None

Writes csv files to outputpath

[Back to top](#top)

[Up](#flybehavior)

[Previous](#write_csv_files)

<a name="female_behaviour"></a>
`female_behaviour(basefilenames, basepath_tracking, basepath_behaviour,
                     outfilename,
                     groupnames=[],
                     yaxlabels_behaviour=[],
                     colours=[['#bb44bb', '#d68ed6'],
                              ['#E3B6E3', '#F8EDF8'], ['#823082', '#E4B5E4'],
                              ['#808080', '#b2b2b2']],
                     hour=True)`

Function to analyse standard female behaviours including:

* egg laying
* time to copulation
* indices of male behaviours towards female
* distance travelled
* pausing


### Parameters:

basefilenames: list of .mat filenames(excluding '.mat' file extension)

basepath_tracking: path to tracking data

basepath_behaviour: path to csv files

outfilename: name for csv file

### Optional Keyword Arguments


groupnames: list of names for the groups, if not equal to filenames (default [])

yaxlabels_behaviour: label of yaxes (default [])

colours: colours for boxplots

 (default: [['#bb44bb', '#d68ed6'],
                              ['#E3B6E3', '#F8EDF8'], ['#823082', '#E4B5E4'],
                              ['#808080', '#b2b2b2']])

hour: whether copulation should be analysed of one hour (default: True)


### Output:

None

Writes csv files to outputpath


[Back to top](#top)

[Up](#flybehavior)

[Previous](#write_indices_csv_files)




outfilename: name for csv file




<a name="female_behaviour"></a>
`female_behaviour(basefilenames, basepath_tracking, basepath_behaviour,
                     outfilename,
                     groupnames=[],
                     yaxlabels_behaviour=[],
                     colours=[['#bb44bb', '#d68ed6'],
                              ['#E3B6E3', '#F8EDF8'], ['#823082', '#E4B5E4'],
                              ['#808080', '#b2b2b2']],
                     hour=True)`

Function to analyse standard female behaviours including:

* egg laying
* time to copulation
* indices of male behaviours towards female
* distance travelled
* pausing


### Parameters:

basefilenames: list of .mat filenames(excluding '.mat' file extension)

basepath_tracking: path to tracking data

basepath_behaviour: path to csv files

outfilename: name for plots generated (will be extended with specific behaviour)

### Optional Keyword Arguments


groupnames: list of names for the groups, if not equal to filenames (default [])

yaxlabels_behaviour: label of yaxes (default [])

colours: colours for boxplots

 (default: [['#bb44bb', '#d68ed6'],
                              ['#E3B6E3', '#F8EDF8'], ['#823082', '#E4B5E4'],
                              ['#808080', '#b2b2b2']])

hour: whether copulation should be analysed of one hour (default: True)


### Output:

None

generate plots and saves them to outputpath


[Back to top](#top)

[Up](#flybehavior)

[Previous](#write_indices_csv_files)


<a name="male_behaviour"></a>
`male_behaviour(basefilenames, basepath_tracking, basepath_behaviour,
                     outfilename,
                     groupnames=[],
                     yaxlabels_behaviour=[],
                     colours=[['#bb44bb', '#d68ed6'],
                              ['#E3B6E3', '#F8EDF8'], ['#823082', '#E4B5E4'],
                              ['#808080', '#b2b2b2']],
                     hour=True)`

Function to analyse standard female behaviours including:

* time to copulation
* indices of male behaviours towards female
* distance travelled of companion female



### Parameters:

basefilenames: list of .mat filenames(excluding '.mat' file extension)

basepath_tracking: path to tracking data

basepath_behaviour: path to csv files

outfilename: name for csv file

### Optional Keyword Arguments


groupnames: list of names for the groups, if not equal to filenames (default [])

yaxlabels_behaviour: label of yaxes (default [])

colours: colours for boxplots

 (default: [['#bb44bb', '#d68ed6'],
                              ['#E3B6E3', '#F8EDF8'], ['#823082', '#E4B5E4'],
                              ['#808080', '#b2b2b2']])

hour: whether copulation should be analysed of one hour (default: True)


### Output:

None

generate plots and saves them to outputpath

[Back to top](#top)

[Up](#flybehavior)

[Previous](#female_behaviour)

<a name="stats"></a>
## Behaviourstats

The Behaviourstats module is written in R. In can be used in jupyter notebook (R installation required).

[egglaying_stats](#egglayingstats)

[indices_stats](#indices_stats)

[Back to top](#top)

<a name="egglayingstats"></a>
`egglayingstats(filenames, datapath)`

stats for egglaying csv files

This function reads multiple files specified as filenames from a datapath and prints stats of egglaying.

### Parameters:

filenames: A list of strings. Contains filenames of csv files

datapath: A string. Path to csv files

###   Examples:


`filenames <- list('eggfile1.csv', 'eggfile2.csv', 'eggfile3.csv')`
`egglaying_stats(filenames, 'path/to/data')`

### Output:

None

prints stats results to terminal

[Back to top](#top)

[Up](#behaviourstat)

<a name="egglayingstats"></a>
`egglaying_stats(filenames, datapath)`

stats for egglaying csv files

This function reads multiple files specified as filenames from a datapath and prints stats of egglaying.

### Parameters:

filenames: A list of strings. Contains filenames of csv files

datapath: A string. Path to csv files

###   Examples:


`filenames <- list('eggfile1.csv', 'eggfile2.csv', 'eggfile3.csv')`
`egglaying_stats(filenames, 'path/to/data')`

### Output:

None

prints stats results to terminal

[Back to top](#top)

[Up](#behaviourstats)

<a name="indices_stats"></a>
`indices_stats(indicesfile, datapath)`

stats for behaviour indices

This function reads indices file from a datapath and prints stats (Kruskal-Wallis and Wilcox) of indices.

### Parameters:

indicesfile A csv file containing indices of behaviour tracking for multiple gentopyes 

datapath: A string. Path to csv files

###   Examples:

`indices_stats(filename, 'path/to/data')`

### Output:

list of p-values for Kruskal-Wallis and Wilcox tests, adjusted for multiple comparisons where appropriate.


[Back to top](#top)

[Up](#behaviourstats)

[Previous](#egglayingstats)
