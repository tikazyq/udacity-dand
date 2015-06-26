# install below packages if not installed
install.packages('scales')
install.packages('memisc')
install.packages('lattice')
install.packages('MASS')
install.packages('car')
install.packages('reshape')
install.packages('plyr')

# load libraries
library(ggplot2)
library(GGally)
library(scales)
library(memisc)

# load data
data("diamonds")

# Scatterplot Review
ggplot(data = diamonds, 
       aes(x = carat, y = price)) + 
  geom_point(fill = I('orange')) +
  stat_smooth(method = 'lm') + 
  ylim(0, quantile(diamonds$price, 0.99)) + 
  xlim(0, quantile(diamonds$carat, 0.99))

# ggpairs Function

# The Demand of Diamonds
library(gridExtra)

plot1 <- qplot(data = diamonds, x = price, binwidth = 100) + 
  ggtitle('Price')

plot2 <- qplot(data = diamonds, x = price, binwidth = 0.01) +
  scale_x_log10() + 
  ggtitle('Price (log10)')

grid.arrange(plot1, plot2, ncol = 1)

