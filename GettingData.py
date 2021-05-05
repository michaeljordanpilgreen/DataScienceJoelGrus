## "To write it, it took three months; to conceive it, three minutes; to collect 
# the data in it, all my life" - F. Scott Fitzgerald
#
# In order to be a data scientist you need data. In fact, as a data scientist you
# will spend an embarrasingly large fraction of your time acquiring, cleaning, and
# transforming data. In a pinch, you can always type the data in yourself (or if you
# have minions, make them do it), but usually this is not a good use of your time.
# In this chapter, we'll look at different ways of getting data into Python and into
# the right formats.
#
# stdin and stdout:
# If you run your Python scripts at the command line, you can pipe data through them
# using sys.stdin and sys.stdout. For example, here is a script that reads in lines
# of text and spits back out the ones that match a regular expression:

# egrep.py
import sys, re

# sys.argv is the list of command-line arguments
# sys.argv[0] is the name of the program itself
# sys.argv[1] will be the regex specified at the command line
regex = sys.argv[1]

# for every line passed into the script
for line in sys.stdin:
    # if it matches the regex, write it to stdout
    if re.search(regex, line):
        sys.stdout.write(line)

# And here's one that counts the lines it receives and then writes out the count:

# line_count.py
import sys

count = 0
for line in sys.stdin:
    count += 1

# print goes to sys.stdout
print count

# You could then use these to count how many lines of a file contain numbers. In
# Windows, you'd use

type SomeFile.txt | python egrep.py "[0-9]" | python line_count.py

# Whereas in a Unix system you'd use:

cat SomeFile.txt | python egrep.py "[0-9]" | python line_count.py

# The | is the pipe character, which means "use the output of the left command as
# the input of the right command." You can build pretty elaborate data-processing
# pipelines this way.
#
# Similarly, here's a script that counts the words in its input and writes out the most
# common ones:

# most_common_words.py
import sys
from collections import Counter

# pass in number of words as first argument
try:
    num_words = int(sys.argv[1])
except:
    print "usage: most_common_words.py num_words"
    sys.exit(1)  # non-zero exit code indicates error

counter = Counter(word.lower() # lowercase words
                    for line in sys.stdin
                    for word in line.strip().split()   # split on spaces
                    if word) # skip empty 'words'

for word, count in counter.most_common(num_words):
    sys.stdout.write(str(count))
    sys.stdout.write("it")
    sys.stdout.write(word)
    sys.stdout.write("\n")

# after which you do something like:

'C:\DataScience>type the_bible.txt | python most_common_words.py 10'

## Reading Files: 
# You can also explicitly read from and write to files directly in your code. Python
# makes working with files pretty simple.
#
# The Basics of Text Files:
# The first step to working with a text file is to obtain a file object using open:

# 'r' means read-only
file_for_reading = open('reading_file.txt', 'r')

# 'w' is write -- will destroy the file if it already exists!
file_for_writing = open('writing_file.txt', 'w')

# 'a' is append -- for adding to the end of the file
file_for_appending = open('appending_file.txt', 'a')

# don't forget to close your files when you're done
file_for_write.close()

## Because it is easy to forget to close your files, you should always use them
# in a with block, at the end of which they will be closed automatically:

with open(filename, 'r') as f:
    data = function_that_gets_data_from(f)
    # at this point f has already been closed, so don't try to use it
    process(data)

# If you need to read whole text file, you can just iterate over the lines of the
# file using for:

starts_with_hash = 0

with open('input.txt', 'r') as f:
    for line in f:
        if re.match("^#",line):
            starts_with_hash += 1
            
# Every line you get this way ends in a newline character, so you'll often want
# to strip() it before doing anything with it.
#
# For example, imagine you have a file full of email addresses, one per line, and
# that you need to generate a histogram of the domains. The rules for correctly
# extracting domains are somewhat subtle (e.g., the Public Suffix List), but a good
# first approximation is to just take the parts of the email addresses that come 
# after the @. (Which gives the wrong answer for email addresses like joel@mail.datascienster.com.)

def get_domain(email_address):
    """split on '@' and return the last piece"""
    return email_address.lower().split("@")[-1]

with open('email_address.txt', 'r') as f:
    domain_counts = Counter(get_domain(line.strip())
                            for line in f
                            if "@" in line)

## Delimited Files: 
# The hypothetical email addresses file we just processed had one address per line.
# More frequently you'll work with files with lots of data on each line. These files
# are very often either comma-separated or tab-separated. Each line has several fields,
# with a comma (or a tab) indicating where one field ends and the next field starts.
#
# This starts to get complicated when you have fields with commas and tabs and
# new-lines in them (which you inevitably do). For this reason, it's pretty much
# always a mistake to try to parse them yourself. Instead, you should use Python's
# csv module (or the pandas library). For technical reasons that you should feel free
# to blame on Miscosoft, you should always work with csv files in binary mode by 
# including a b after the r or w.
#
# If your file has no headers (which means you probably want each row as a list,
# and which places the burden on you to know what's in each column), you can use
# csv.reader to iterate over the rows, each of which will be an appropriately split
# list.
#
# For example, if we had a tab-delimited file of stock prices:
# we could process them with:
import csv

with open('tab_delimited_stock_prices.txt', 'rb') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        date = row[0]
        symbol = row[1]
        closing_price = float(row[2])
        process(date, symbol, closing_price)

# If your file has headers: you can either skip the header row (with an initial call
# to reader.next()) or get each row as a dict (with the headers as keys) by using
# csv.DictReader:

with open('colon_delimited_stock_prices.txt', 'rb') as f:
    reader = csv.DictReader(f, delimiter=':')
    for row in reader:
        date = row["date"]
        symbol = row["symbol"]
        closing_price = float(row["closing_price"])
        process(date, symbol, closing_price)

# Even if your file doesn't have headers you can still use DictReader by passing it
# the keys as a fieldnames parameter.
#
# You can similarly write out delimited data using csv.writer:

today_prices = { 'AAPL' : 90.91, 'MSFT' : 41.68, 'FB' : 64.5 }

with open('comma_delimited_stock_prices.txt', 'wb') as f:
    writer = csv.writer(f, delimiter=',')
    for stock, price in today_prices.items():
        writer.writerow([stock, price])

# csv.writer will do the right thing if your fields themselves have commas in them.
# Your own hand-rolled writer probably won't. For example, if you attempt:

results = [["test1", "success", "Monday"],
            ["test2", "success, kind of", "Tuesday"],
            ["test3", "failure, kind of", "Wednesday"],
            ["test4", "failure, utter", "Thursday"]]\

# don't do this
with open('bad_csv.txt', 'w') as f:
    for row in results:
        f.write(",".join(map(str, row))) # might have too many commas in it!
        f.write("\n")                    # row might have newlines as well!
# You will end up with a csv file that looks like:
test1,success,Monday
test2,success, kind of,Tuesday...
# and that no one will ever be able to make sense of.

## Scraping the Web:
# Another way to get data is by scraping it from web pages. Fetching web pages, it 
# turns out, is pretty easy; getting meaningful structured information out of them
# less so.
#
# HTML and the Parsing Thereof:
# Pages on the web are written in HTML, in which text is (ideally) marked up into 
# elements and their attributes:
#
# In a perfect world, where all web pages are marked up samantically for our benefit,
# we would be able to extract data using rules like "find the <p> element whose id
# is subjkect and return the text it contains." In the actual world, HTML, is not
# generally well-formed, let alone annotated. This means we'll need help making sense
# of it.
#
# To get data out of HTML, we will use the BeautifulSoup library (http://www.crummy.com/software/BeautifulSoup),
# which builds aa tree out of the various elements on a web page and provides a simple
# interface for accessing them. As I write this, the latest version is Beautiful Soup
# 4.3.2 (pip install beautifulsoup4), which is what we'll be using. We'll also be 
# using the requests library (pip install requests), which is a much nicer way of 
# making HTTP requests than anything that's built into Python.
#
# Python's built-in HTML parser is not that lenient, which means that it doesn't
# always cope well with HTML that's not perfectly formed. For that reason, we'll
# use a different parser, which we need to install:

pip install htmlSlib

# To use Beautiful Soup, we'll need to pass some HTML into the BeautifulSoup() 
# function. In our examples, this iwll be the result of a call to requests.get:

from bs4 import BeautifulSoup
import requests
html = requests.get("http://www.example.com").text
soup = BeautifulSoup(html, 'html5lib')

# after which we can get pretty far using a few simple methods.