## "Experts often posses more data than judgement." -Colin Powell
# Working with data is both an art and a science. We've mostly been talking about 
# the science part, but in this chapter we'll look at some of the art.
#
# Exploring Your Data:
# After you've identified the questions you're trying to answer and have gotten
# your hands on some data, you might be tempted to dive in and immediately
# start building models and getting answers. But you should resist this urge.
# Your first step should be to explore your data.
#
# Exploring One-Dimensional Data:
# The simplest case is when you have a one-dimensional data set, which is just a
# collection of numbers. For example, these could be the daily average number of
# minutes each user spends on your site, the number of times each of a collection
# of data science tutorial videos was watched, or the number of pages of each of
# the data science books in your data science library.
#
# An obvious first step is to compute a few summary statistics. You'd like to know
# how many data points you have, the smallest, the largest, the mean, and the 
# standard deviation.
#
# But even these don't necessarily give you a great understanding. A good next
# step is to create a histogram, in which you group your data into discrete 
# buckets and count how many points fall into each bucket:

def bucketsize(point, bucket_size):
    """floor the point to the next lower multiple of bucket_size"""
    return bucket_size * math.floor(point / bucket_size)

def make_histogram(points, bucket_size):
    """buckets the points and counts how many in each bucket"""
    return Counter(bucketsize(point, bucket_size) for point in points)

def plot_histogram(points, bucket_size, title=""):
    histogram = make_histogram(points, bucket_size)
    plt.bar(histogram.keys(), histogram.values(), width=bucket_size)
    plt.title(title)
    plt.show()

# For example, consider the two following sets of data:

random.seed(0)

# uniform between -100 and 100
uniform = [200 * random.random() - 100 for _ in range(10000)]

# normal distribution with mean 0, standard deviation 57
normal = [57 * inverse_normal_cdf(random.random())
        for _ in range(10000)]

# Both have means close to 0 and standard deviations close to 58. However, they
# have very different distributions. Figure 10-1 shows the distributions of uniform:

plot_histogram(uniform, 10, "Uniform Histogram")

# while 10-2 shows the distribution of normal:

plot_histogram(normal, 10, "Normal Histogram")

# In this case, both distributions had pretty different max and min, but even 
# knowing that wouldn't have been sufficient to understand how they differed.
#
# Two Dimensions:
# Now imagine you have a data set with two dimensions. Maybe in addition to daily
# minutes you have years of data science experience. Of course you'd want to understand
# each dimension individually. But you probably also want to scatter the data.
#
# For example, consider another fake data set:

def random_normal():
    """returns a random draw from a standard normal distribution"""
    return inverse_normal_cdf(random.random())

xs = [random_normal() for _ in range(1000)]
ys1 = [ x + random_normal() / 2 for x in xs]
ys2 = [ -x + random_normal() / 2 for x in xs]

# If you were to run plot_histogram on ys1 and ys2 you'd get very similar looking
# plots (indeed, both are normally distributed with the same mean and standard
# deviation).
#
# But each has a very different joint distribution with xs, as show in figure 10-3

plt.scatter(xs, ys1, marker='.', color='black', label='ys1')
plt.scatter(xs, ys2, marker='.', color='gray', label='ys2')
plt.xlabel('xs')
plt.ylabel('ys')
plt.legend(loc=9)
plt.title("Very Different Joint Distributions")
plt.show()

# This difference would also be apparent if you lookded at the correlations:

print correlation(xs, ys1)
print correlation(xs, ys2)

# Many Dimensions:
# With many dimensions, you'd like to know how all the dimensions relate to one 
# another. A simple approach is to look at the correlation matrix, in which the
# entry in row i and column j is the correlation between the ith dimension and 
# the jth dimension of the data:

def correlation_matrix(data):
    """returns the num_columns x num_columns matrix whose (i, j)th entry 
    is the correlation between columsn i and j of data"""

    _, num_columns = shape(data)

    def matrix_entry(i, j):
        return correlation(get_column(data, i), get_column(data, j))

    return make_matrix(num_columns, num_columns, matrix_entry)

# A more visual approach (if you don't have too many dimensions) is to make a
# scatterplot matrix (figure 10-4) showing all the pairwise scatterplots. To do
# that we'll use plt.subplot(), which allows us to create subplots of our chart.
# We give it the number of rows and the number of columns, and it returns a figure
# object ( which we won't use ) and a two-dimensional array of axes objects (each
# of which we'll plot to):

import matplotlib.pyplot as plt 

_, num_columns = shape(data)
fig, ax = plt.subplots(num_columns, num_columns)

for i in range(num_columns):
    for j in range(num_columns):

        # scatter column_j on the x-axis vs column_i on the y-axis
        if i != j: ax[i][j].scatter(get_column(data, j), get_column(data, i))

        # unless i == j, in which case show the series name
        else: ax[i][j].annotate("series " + str(i), (0.5, 0.5),
                                xycoords='axes fraction',
                                ha="center", va="cemter")
        
        # then hide axis labels except left and bottom charts
        if i < num_columns - 1: ax[i][j].xaxis.set_visible(False)
        if j > 0: ax[i][j].yaxis.set_visible(False)
    
    # fix the bottom right and top left axis labels, which are wrong because
    # their charts only have text in them
    ax[-1][-1].set_xlim(ax[0][-1].get_xlim())
    ax[0][0].set_ylim(ax[0][1].get_ylim())

    plt.show()
