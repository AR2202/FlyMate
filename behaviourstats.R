library(ggplot2)
library(lme4)
library(dplyr)
library(readxl)
library(tibble)
library(readr)
library(tidyr)
library(rstatix)

#' reading egglaying csv files
#'
#' This function reads multiple files specified as filenames from a datapath and prints statistical analysis results
#' @param filenames A list of strings. Contains filenames of csv files
#' @param datapath A string. Path to csv files
#' @return Returns a dataframe. egg counts
#' @examples
#' # filenames <- list('eggfile1.csv', 'eggfile2.csv', 'eggfile3.csv')
#' egg_df <- egglaying_df(filenames, 'path/to/data')

egglaying_df <- function(filenames, datapath) {
   filepaths <- lapply( filenames, function(x) file.path(datapath, x))
   my_data <- lapply(filepaths, read_csv)
   for(i in 1:length(my_data)) {
   my_data[[i]] <- my_data[[i] ] %>% 
      mutate(group = i)
   my_data[[i]]$group <-factor(my_data[[i]]$group)
  
}
   
   egg_df <- do.call('rbind',my_data)%>% rename(day1 = `24h`)%>% rename(day2 = `48h`)%>% mutate(total= day1 +day2)
   return(egg_df)
}

#' stats for egglaying csv files
#'
#' This function reads multiple files specified as filenames from a datapath and returns a dataframe of egg counts
#' @param filenames A list of strings. Contains filenames of csv files
#' @param datapath A string. Path to csv files
#' #' @examples
#' # filenames <- list('eggfile1.csv', 'eggfile2.csv', 'eggfile3.csv')
#'  egglaying_stats(filenames, 'path/to/data')

egglaying_stats <- function(filenames, datapath) {
   egg_df <- egglaying_df(filenames, datapath)
   linear_model_eggs <- lm(total ~group, data = egg_df)
   summary(linear_model_eggs)
   pairewiset <- egg_df %>% pairwise_t_test(total~ group,p.adjust.method = "holm")
   pairewiset
   
}
# Some sample data
eggfile = "aDN_Chrimson_Female_lighton_egglaying.csv"
eggfile2 = "Otd_Chrimson_Female_lighton_egglaying.csv"
eggfile3 = "aDN_stop_Chrimson_Female_lighton_egglaying.csv"
behaviourpath = "/Volumes/LaCie/Projects/aDN_MB/behaviour/"

filenames <- list(eggfile, eggfile2, eggfile3)
egglaying_stats(filenames, behaviourpath)