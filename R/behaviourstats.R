library(ggplot2)
library(lme4)
library(dplyr)
library(readxl)
library(tibble)
library(readr)
library(tidyr)
library(rstatix)

#' reading csv files to dataframe
#'
#' This function reads multiple files specified as filenames from a datapath and returns dataframe list
#' @param filenames A list of strings. Contains filenames of csv files
#' @param datapath A string. Path to csv files
#' @return Returns a dataframe. egg counts
#' @examples
#' # filenames <- list('eggfile1.csv', 'eggfile2.csv', 'eggfile3.csv')
#' dfs <- csvs_to_df(filenames, 'path/to/data')
csvs_to_df <- function(filenames, datapath){
   filepaths <- lapply( filenames, function(x) file.path(datapath, x))
   my_data <- lapply(filepaths, read_csv)
   for(i in 1:length(my_data)) {
   my_data[[i]] <- my_data[[i]] %>% 
      mutate(group = i)
   my_data[[i]]$group <- factor(my_data[[i]]$group)
   }
   return(my_data)

}
#' reading egglaying csv files
#'
#' This function reads multiple files specified as filenames from a datapath and returns dataframe of egg counts
#' @param filenames A list of strings. Contains filenames of csv files
#' @param datapath A string. Path to csv files
#' @return Returns a dataframe. egg counts
#' @examples
#' # filenames <- list('eggfile1.csv', 'eggfile2.csv', 'eggfile3.csv')
#' egg_df <- egglaying_df(filenames, 'path/to/data')

egglaying_df <- function(filenames, datapath) {
   my_data <- csvs_to_df(filenames, datapath)
   egg_df <- do.call('rbind',my_data) %>% 
      rename(day1 = `24h`) %>%
      rename(day2 = `48h`) %>%
      mutate(total = day1 +day2)
   return(egg_df)
}

#' stats for egglaying csv files
#'
#' This function reads multiple files specified as filenames from a datapath and prints stats of egglaying
#' @param filenames A list of strings. Contains filenames of csv files
#' @param datapath A string. Path to csv files
#' #' @examples
#' # filenames <- list('eggfile1.csv', 'eggfile2.csv', 'eggfile3.csv')
#'  egglaying_stats(filenames, 'path/to/data')

egglaying_stats <- function(filenames, datapath) {
   egg_df <- egglaying_df(filenames, datapath)
   linear_model_eggs <- lm(total ~group, data = egg_df)
   summary(linear_model_eggs)
   pairewiset <- egg_df %>% 
      pairwise_t_test(total~ group,p.adjust.method = "holm")
   pairewiset
   
}
#' stats for indices csv files
#'
#' This function readindices file specified as filenames from a datapath and prints stats of indices
#' @param indicesfile A csv file containing indices of behaviour tracking for multiple gentopyes 
#' (as output by python function flybehaviour.write_indices_csv_file)
#' @param datapath A string. Path to csv file
#' #' @examples
#'  indices_stats(filename, 'path/to/data')
indices_stats <- function(indicesfile, datapath) {
   indicespath = file.path(trackingpath, indicesfile)
   indices <- read_csv(indicespath)
   data_indices <- subset( indices, select = -group )
   kw <- sapply(data_indices, function(x) kruskal.test(x ~ indices$group))
   pvals = kw[3,]
   pvals_adj = list()
   pvals_adj$kruskal = p.adjust(pvals, "holm")
 
   pvals_adj$wilcox <- sapply(data_indices, function(x) pairwise.wilcox.test(x,indices$group, p.adjust.method = "BH"))
   return (pvals_adj)
   # todo - multiple comparison correction
   

}
