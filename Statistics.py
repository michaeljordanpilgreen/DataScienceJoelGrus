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