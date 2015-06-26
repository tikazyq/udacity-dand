library(dplyr)
library(ggplot2)
library(reshape2)
library(GGally)

pf = read.csv('pseudo_facebook.tsv', sep='\t')

# Third Qualitative Variable
pf.fc_by_age_gender <- pf %>%
  group_by(age, gender) %>%
  summarise(mean_friend_count = mean(friend_count),
            median_friend_count = median(friend_count) * 1.0,
            n = n()) %>%
  ungroup() %>%
  arrange(age)

# Plotting Conditional Summaries
ggplot(data = subset(pf.fc_by_age_gender, !is.na(gender)), 
       aes(x=age, y=mean_friend_count, color=gender)) +
  geom_line()

# Reshaping Data
pf.fc_by_age_gender.wide <- dcast(pf.fc_by_age_gender, 
                                  age ~ gender, 
                                  value.var = 'median_friend_count')
head(pf.fc_by_age_gender.wide)

# Ratio Plot
## plotting
pf.fc_by_age_gender.wide$ratio <- pf.fc_by_age_gender.wide$female / pf.fc_by_age_gender.wide$male
ggplot(data = pf.fc_by_age_gender.wide, aes(x = age, y = ratio)) + 
  geom_line() + 
  geom_hline(aes(yintercept = 1), linetype=2)

# Third Quantitative Variable
pf$year_joined <- as.integer(2014 - pf$tenure / 365)

# Cut a Variable
pf$year_joined.bucket <- cut(pf$year_joined, breaks = c(2004, 2009, 2011, 2012, 2014))

# Plotting It All Together
pf.fc_by_age_year_joined <- pf %>%
  group_by(age, year_joined.bucket) %>%
  summarise(mean_friend_count = mean(friend_count)) %>%
  ungroup()
ggplot(data = na.omit(pf.fc_by_age_year_joined), 
       aes(x = age, y = mean_friend_count, color = year_joined.bucket)) + 
  geom_line()

# Plot the Grand Mean
ggplot(data = subset(pf, !is.na(year_joined.bucket)), 
       aes(x = age, y = friend_count)) + 
  geom_line(stat = 'summary', fun.y = mean,
            aes(color = year_joined.bucket)) + 
  geom_line(stat = 'summary', 
            fun.y = mean, 
            linetype = 2, 
            alpha = 0.5)

# Friending Rate
pf$friending_rate <- pf$friend_count / pf$tenure
summary(subset(pf, tenure > 0)$friending_rate)

# Friendships Initiated
pf$friendships_initiated_per_day <- pf$friendships_initiated / pf$tenure
ggplot(data = subset(pf, tenure >= 1),
       aes(x = tenure, y = friendships_initiated_per_day)) + 
  geom_line(
    stat = 'summary',
    fun.y = mean,
    aes(color = year_joined.bucket))

# Bias Variance Trade off Revisited
ggplot(aes(x = 7 * round(tenure / 7), y = friendships_initiated / tenure),
       data = subset(pf, tenure > 0)) +
  geom_smooth(aes(color = year_joined.bucket))

# Histograms Revisited
yo <- read.csv('yogurt.csv')
yo$id <- factor(yo$id)
str(yo)
## plotting
qplot(x = price, data = yo)
## findings
### The distribution contains quite a lot of discreteness. 

# Number of Purchases
yo <- transform(yo, all.purchases = strawberry + blueberry + pina.colada + plain + mixed.berry)

# Prices Over Time
ggplot(data = yo, aes(x = time, y = price)) +
  geom_point(alpha=0.1, position = 'jitter')

# Looking at Samples of Households
set.seed(4230)
sample.ids <- sample(levels(yo$id), 16)
ggplot(subset(yo, id %in% sample.ids), aes(x = time, y = price)) + 
  facet_wrap(~ id) + 
  geom_line() + 
  geom_point(aes(size = all.purchases), pch = 1)

# Scatterplot Matrices
library(GGally)
theme_set(theme_minimal(20))

set.seed(1836)
pf_subset <- pf[, c(2:15)]
names(pf_subset)
ggpairs(pf_subset[sample.int(nrow(pf_subset), 1000), ])

# Create a Heat Map
nci <- read.table('nci.tsv')
colnames(nci) <- c(1:64)
nci.long.samp <- melt(as.matrix(nci[1:200, ]))
names(nci.long.samp) <- c('gene', 'case', 'value')
## plotting
ggplot(aes(y = gene, x = case, fill = value),
       data = nci.long.samp) + 
  geom_tile() + 
  scale_fill_gradientn(colours = colorRampPalette(c('blue', 'red'))(100))
