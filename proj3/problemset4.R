library(ggplot2)
library(gridExtra)
library(dplyr)

data("diamonds")

# price vs x
## plotting
ggplot(aes(x = price, y = x), data = diamonds) +
  geom_point(alpha = 0.02) + 
  scale_x_continuous(breaks = seq(0, 20000, 2000)) + 
  scale_y_continuous(breaks = seq(0, 10, 1))

## findings
### exponential relationship between price and x

## correlations
print(cor.test(diamonds$price, diamonds$x))
### 0.8844352 
print(cor.test(diamonds$price, diamonds$y))
### 0.8654209 
print(cor.test(diamonds$price, diamonds$z))
### 0.8612494 


# price vs. depth
## plotting
ggplot(aes(x = price, y = depth), data = diamonds) +
  geom_point(alpha = 0.01) +
  scale_x_continuous(breaks = seq(0, 20000, 2000)) #+ 
  # scale_y_continuous(breaks = seq(0, 10, 1))

## correlation
print(cor.test(diamonds$price, diamonds$depth))


# price vs. caret
## plotting
ggplot(aes(x = price, y = carat), data = diamonds) +
  geom_point(alpha = 0.05) +
  scale_x_continuous(breaks = seq(0, 20000, 2000)) + 
  scale_y_continuous(breaks = seq(0, 5, 1))


# price vs. volume
diamonds$volume = diamonds$x * diamonds$y * diamonds$z

## plotting
ggplot(aes(x = price, y = volume), data = diamonds) +
  geom_point(alpha = 0.01) +
  scale_x_continuous(breaks = seq(0, 20000, 2000)) + 
  coord_cartesian(ylim = c(0, 500))

## findings
### there are extreme outliers, with volume near 1000 and near 4000, which seems to be bad data points.
### exponential relationship between price and volume

## correlations
diamonds.good <- subset(diamonds, volume > 0 & volume < 800)
print(cor.test(diamonds.good$price, diamonds.good$volume))
 
## linear model
ggplot(aes(x = price, y = volume), data = diamonds) +
  geom_point(alpha = 0.01) +
  geom_smooth() +
  scale_x_continuous(breaks = seq(0, 20000, 2000)) + 
  coord_cartesian(ylim = c(0, 500))

# Mean Price by Clarity
diamondsByClarity <- group_by(diamonds, clarity) %>%
  summarise(mean_price = mean(price),
            median_price = median(price), 
            min_price = min(price), 
            max_price = max(price), 
            n = n()
            )

# Bar Charts of Mean Price
data(diamonds)
library(dplyr)

diamonds_by_clarity <- group_by(diamonds, clarity)
diamonds_mp_by_clarity <- summarise(diamonds_by_clarity, mean_price = mean(price))

diamonds_by_color <- group_by(diamonds, color)
diamonds_mp_by_color <- summarise(diamonds_by_color, mean_price = mean(price))

## plotting
p1 = ggplot(diamonds_mp_by_clarity, aes(x=clarity, y = mean_price)) + geom_bar(stat = 'identity')
p2 = ggplot(diamonds_mp_by_color, aes(x=color, y = mean_price)) + geom_bar(stat = 'identity')
grid.arrange(p1, p2, ncol=1)

## findings
### The mean price is maximum at clarity of SI2 and color of J.
# We think something odd is going here. These trends seem to go against our intuition.
# Mean price tends to decrease as clarity improves. The same can be said for color.
# We encourage you to look into the mean price across cut.
ggplot(diamonds_mp_by_clarity, aes(x=clarity, y = mean_price)) + geom_bar(stat = 'identity')
ggplot(diamonds, aes(y=price, x=clarity)) + geom_jitter(alpha=0.05)
