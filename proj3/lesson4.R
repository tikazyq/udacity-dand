# load libraries
library(ggplot2)
library(dplyr)
library(gridExtra)

# load data
pf <- read.csv('pseudo_facebook.tsv', sep='\t')

# temp vs month
library(alr3)
data("Mitchell")
ggplot(data = Mitchell, aes(x = Month, y = Temp)) + geom_point()

# test correlation coefficient
print(cor.test(Mitchell$Month, Mitchell$Temp))

# Making sense of data
ggplot(data = Mitchell, aes(x = Month, y = Temp)) + 
  geom_point() + 
  scale_x_discrete(breaks=seq(0, 203, 12))

# Understanding the Noise: Age to Age Months
pf$age_with_months <- pf$age + (12 - pf$dob_month) / 12

# Age Means
pf.fc_by_age <- group_by(pf, age) %>%
  summarise(friend_count_mean = mean(friend_count),
            friend_count_median = median(friend_count),
            n = n())

# Age with Months Means
pf.fc_by_age_months <- group_by(pf, age_with_months) %>%
  summarise(friend_count_mean = mean(friend_count),
            friend_count_median = median(friend_count),
            n = n()) 

x = seq_along(pf.fc_by_age_months$friend_count_mean)

p1 = ggplot(aes(age_with_months, friend_count_mean), 
       data = subset(pf.fc_by_age_months, age_with_months < 70)) +
  geom_line()

p2 = ggplot(aes(age, friend_count_mean), 
       data = subset(pf.fc_by_age, age < 70)) +
  geom_line()

grid.arrange(p1, p2, ncol = 1)
