library(dplyr)
library(ggplot2)
library(reshape2)
library(GGally)

data(diamonds)


# Price Histograms with Facet and Color
ggplot(data = diamonds, 
       aes(x = price, fill = cut)) + 
  geom_histogram() + 
  facet_wrap(~ color) +
  scale_fill_brewer(type = 'qual')

# Price vs. Table Colored by Cut
ggplot(data = diamonds, 
       aes(x = table, y = price, color = cut)) + 
  geom_point() +
  scale_color_brewer(type = 'qual') + 
  scale_x_continuous(breaks = seq(44, 86, 2)) + 
  coord_cartesian(xlim = c(45, 85))

# Price vs. Volume and Diamond Clarity
diamonds <- transform(diamonds, volume = x * y * z)
diamondsExclTop1Pct <- arrange(diamonds, desc(volume))[as.integer(0.01 * (nrow(diamonds))):nrow(diamonds), ]
ggplot(data = subset(diamondsExclTop1Pct), 
       aes(x = volume, y = price, color = clarity)) + 
  geom_point() + 
  scale_color_brewer(type = 'div') + 
  scale_x_continuous(breaks = c(0, 1000, 10000)) + 
  coord_trans(y = 'log10')

# Proportion of Friendships Initiated
pf <- read.csv('pseudo_facebook.tsv', sep='\t')
pf$prop_initiated <- pf$friendships_initiated / pf$friend_count

# prop_initiated vs. tenure
pf$year_joined <- 2014 - pf$tenure / 365
pf$year_joined.bucket <- cut(pf$year_joined, breaks = c(2004, 2009, 2011, 2012, 2014))
ggplot(data = subset(pf, !is.na(year_joined.bucket)), 
       aes(x = tenure, y = prop_initiated)) + 
  geom_line(stat = 'summary', fun.y = mean, 
            aes(color = year_joined.bucket))

# Smoothing prop_initiated vs. tenure
ggplot(data = subset(pf, !is.na(year_joined.bucket))) +  
  geom_line(stat = 'summary', fun.y = mean, 
            aes(x = 10 * round(tenure / 10), y = prop_initiated, color = year_joined.bucket))  

# Largest Group Mean prop_initiated
by(pf$friendships_initiated, pf$year_joined.bucket, sum) 
by(pf$prop_initiated, pf$year_joined.bucket, summary) 
## the group with the largest proportion of friend_initiated is (2012, 2014]
summary(subset(pf, year_joined.bucket = '(2012, 2014]')$prop_initiated)

# Price/Carat Binned, Faceted, & Colored
ggplot(data = diamonds, 
       aes(x = cut, y = price / carat, color = color)) + 
  geom_point(position = position_jitter(h = 0)) + 
  facet_wrap(~ clarity) + 
  scale_color_brewer('qual')

