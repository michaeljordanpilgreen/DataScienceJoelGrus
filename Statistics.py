##Central Tendencies: Usually, we'll want some notion of where our data is centered. Most commonly we'll
# use the mean (or average), which is just the sum of the data dividied by its count:

# this isn't right if you don't from __future__ import division
def mean(X):
    return sum(x) / len(x)

mean(num_friends)

## If you have two data points, the mean is simply the point halfway between them. As you add more points,
# the mean shifts around, but it alwaysd depends on the value of every point.
#
# We'll also sometimes be interested in the median, which is the middle-most value (if the number of data
# points is odd) or the average of the two middle-most values (if the number of data points is even)
#
# For instance, if we have five data points in a sorted vector x, the median is x[5 // 2] or x[2]. IF we
# have six data points, we want the average of x[2] (the third point) and x[3] (the fourth point).
# 
# Notice that - unlike the mean - the median doesn't depend on every value in your data. For example,
# if you make the largest point larger (or the smallest opint smaller), the middle points remain unchanged,
# which means so does the median.
#
# The median function is slightly more complicated than you might expect, mostly because of the "even"
# case:

def median(v):
    """finds the 'middle-most' value of v"""
    n = len(v)
    sorted_v = sorted(v)
    midpoint = n // 2

    if n % 2 == 1:
        # if odd, return the middle value
        return sorted_v[midpoint]
    else:
        # if even, return the average opf the middle values
        lo = midpoint - 1
        hi = midpoint
        return (sorted_v[lo] + sorted_v[hi]) / 2
        
    median(num_friends)

## Clearly, the mean is simpler to compute, and it varies smoothly as our data changes. If we have n data
# points and one of them increases by some small amount e, then necessarily the mean will increase by 
# e / n. (This makes the mean amenable to all sorts of calculus tricks.) Whereas in order to find the median,
# we have to sort our data. And changing one of our data points by a small amount e might increase the median
# by e, by some number less than e, or not at all (depending on the rest of the data).
#
# At the same time, the mean is very sensitive to outliers in our data. If our friendliest user had 200 
# friends (instead of 100), then the mean would rise to 7.82, while the median would stay the same. If
# outliers are likely to be bad data (or otherwise unrepresentative of whatever phenomenon we're trying
# to understand), then the mean can sometimes give us a misleading picture. For example, the story is often
# told that in the mid-1980s, the major at the University of North Carolina with the highest average
# starting salary was geography, mostly on account of NBA star (and outlier) Michael Jordan.
#
# A generalization of the median is the quantile, which represents the value less than which a ceratin
# percentile of the data lies. ( The median represents the value less than which 50% of the data lies.)

def quantile(x, p):
    """returns the pth-percentile value in x"""
    p_index = int(p * len(x))
    return sorted(x)[p_index]

quantile(num_friends, 0.10)
quantile(num_friends, 0.25)
quantile(num_friends, 0.75)
quantile(num_friends, 0.90)

# Less commmonly you might want to look at the mode, or most-common value[s]:

def mode(x):
    """returns a list, might be more than one mode"""
    counts = Counter(x)
    max_count = max(counts.values())
    return [x_i for x_i, count in counts.iteritems()
            if count == max_count]

mode(num_friends)

# But most frequently we'll just use the mean.

## Dispersion: Dispersion referes to measures of how spread out our data is. Typically
# they're statistics for which values near zero signify not spread out at all and for 
# for which large values (whatever that means) signify very spread out. For instance,
# a very simple measure is the range, which is just the difference between the largest
# and smallest elements:

# "range" akready means something in Python, so we'll use a different name
def data_range(x):
    return max(x) - min(x)

data_range(num_friends)

## The rang eis zero precisely when the max and min are equal, which can only happen
# if the elements of x are all the same, which means the data is an undispersed as possible.
# Conversely, if the range is large, then the max is much larger than the min and the]
# data is more spread out.
# 
# Like the median, the range doesn't really depend on the whole data set. A data set
# whose points are all either 0 or 100 has the same range as a data set whose values are
# 0, 100, and lots of 50s. But it seems like the first data set "should" be more spread out.
#
# A more complex measure of dispersion is the variance, which is computed as:

def de_mean(x):
    """translate x by subtracting its mean (so the result has mean 0)"""
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]

def variance(x):
    """assumes x has at least two elements"""
    n = len(x)
    deviations = de_mean(x)
    return sum_of_squares(deviations) / (n - 1)

variance(num_friends)

## Now, whatever units our data is in (e.g. "friends"), all of our measures of central 
# tendency are in that same unit. THe range will similarly be in the same unit. The 
# variance, on the other hand, has units that are the square of the original units
# (e.g. "friends squared"). As it can be hard to make sense of these, we often look 
# instead at the standard deviation.

def standard_deviation(x):
    return math.sqrt(variance(x))

standard_deviation(num_friends)

## Both the range and the standard deviation have the same outlier problem that we saw
# earlier for the mean. Using the same example, if our friendliest user has instead
# 200 friends, the standard deviation would be 14.89, more than 60% higher!
#
# A more robust alternative computes the difference between the 75th percentile value
# and the 25th percentile value:

def interquartile_range(x):
    return quantile(x, 0.75) - quantile(x, 0.25)

interquartile_range(num_friends)

# which is quite plainly unaffected by a small number of outliers.

## Correlation: Datasciencester's VP of Growth has a theory that the amount of time 
# people spend on the site is related to the number of friends they have on the site
# (she's not a VP for nothing), and she's asked you to verify this.
#
# After digging through traffic logs, you've come up with a list daily_minutes that 
# shows how many minutes per day each user spends on DataSciencester, and you've 
# ordered it so that its elements correspond to the elements of our previous num_friends
# list. We'd like to investigate the relationship between the two metrics.
#
# We'll first look at covariance, the paired analogue of variance. Whereas variance
# measures how a single variable deviates from its mean, covariance measures how two
# variables vary in tandem from their means:

def covariance(x, y):
    n = len(x)
    return dot(de_mean(x), de_mean(y)) / (n - 1)

covariance(num_friends, daily_minutes)

## Recall that dot sums up the products of corresponding pairs of elements. When
# corresponding elements of x and y are either both above their means or both below 
# their means, a positive number enters the sum. When one is above its mean and the other
# below, a negative number enters the sum. Accordingly, a "large" positive covariance
# means that x tends to be large when y is large and small when y is small. A "large"
# negative covariance means the opposite - that x tends to be small when y is large and
# vice versa. A covariance close to zero means that no such relationship exists.
#
# Nonetheless, this number can be hard to interpret, for a couple of reasons.
#  - Its units are the product of the inputs' units (e.g. friend-minutes-per-day),
# which can be hard to make sense of.
#  - If each user had twice as many friends (but the same number of minutes), the 
# covariance would be twice as large. But in a sense the variables would be just as
# interrelated. Said differently, it's hard to say what counts as a "large" covariance.
#
#  For this reason, it's more common to look at the correlation, which divides out the
# standard deviations of both variables:

def correlation(x, y):
    stdev_x = standard_deviation(x)
    stdev_y = standard_deviation(y)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(x, y) / stdev_x / stdev_y
    else:
        return 0 # if no variation, correlation is zero
    
correlation(num_friends, daily_minutes)

## The correlation is unitless and always lies between -1 (perfect anti-correlation)
# and 1 (perfect correlation). A number like 0.25 represents a relatively weak positive
# correlation.
#
# However, one thing we neglected to do was examine our data.
#
# The person with 100 friends (who spends only one minute per day on the site) is 
# a huge outlier, and correlation can be very sensitive to outliers. What happens
# if we ignore him?

outlier = num_friends.index(100)

num_friends_good = [x
                    for i, x in enumerate(num_friends)
                    if i != outlier]

daily_minutes_good = [x
                    for i, x in enumerate(daily_minutes)
                    if i != outlier]

correlation(num_friends_good, daily_minutes_good)

# Without the outlier, there is a much stronger correlation.
#
# You investigate further and discover that the outlier was actually an internal
# test account that no one ever bothered to remove. So you feel pretty justified
# in excluding it.
#
# Simpson's Paradox:
# One not uncommon surprise when analyzing data is Simpson's Paradox, in which 
# correlations can be misleading when confounding variables are ignored.
#
# For example, imagine that you can identify all of your members as either East Coast
# data scientists or West Coast data scientists. You decide to examine which coast's
# data scientists are friendlier:
