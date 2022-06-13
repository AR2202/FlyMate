library(ggplot2)
library(lme4)
library(dplyr)
library(readxl)
library(tibble)
library(readr)
library(tidyr)
library(rstatix)

eggfile = "aDN_Chrimson_Female_lighton_egglaying.csv"
eggfile2 = "Otd_Chrimson_Female_lighton_egglaying.csv"
eggfile3 = "aDN_stop_Chrimson_Female_lighton_egglaying.csv"
behaviourpath = "/Volumes/LaCie/Projects/aDN_MB/behaviour/"

filepath = file.path(behaviourpath, eggfile)
filepath2 = file.path(behaviourpath, eggfile2)
filepath3 = file.path(behaviourpath, eggfile3)
df <- read_csv(filepath)
df2 <- read_csv(filepath2)
df3 <- read_csv(filepath3)

tidy_df <- df %>%
   mutate(group = 0) 
tidy_df$group <- factor(tidy_df$group)


tidy_df2 <- df2 %>%
   mutate(group = 1)
tidy_df2$group <- factor(tidy_df2$group)

tidy_df3 <- df3 %>%
   mutate(group = 2)
tidy_df3$group <- factor(tidy_df3$group)

combined = rbind(tidy_df, tidy_df2, tidy_df3)%>% rename(day1 = `24h`)%>% rename(day2 = `48h`)%>% mutate(total= day1 +day2)
combined

linear_model <- lm(total ~group, data = combined)
summary(linear_model)
pairewiset <- combined %>% pairwise_t_test(total~ group,p.adjust.method = "holm")
pairewiset