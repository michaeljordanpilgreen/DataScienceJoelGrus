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
#
# We'll typically work with Tag objects, which correspond to the tags representing
# the structure of an HTML page.
#
# For example, to find the first <p> tag (and its contents) you can use:

first_paragraph = soup.find('p')   # or just soup.p

# You can get the text contents of a Tag using its text property:

first_paragraph_text = soup.p.text
first_paragraph_words = soup.p.text.split()

# And you can extract a tag's attributes by treating it like a dict:

first_paragraph_id = soup.p['id']   # raises KeyError if no 'id'
first_paragraph_id2 =  soup.p.get('id')  # returns None if no 'id'

# You can get multiple tags at once:

all_paragraphs = soup.find_all('p') # or just soup('p')
paragraphs_with_ids = [p for p in soup('p') if p.get('id')]

# Frequently you'll want to find tags with a specific class:

important_paragraphs = soup('p', {'class' : 'important'})
important_paragraphs2 = soup('p', 'important')
important_paragraphs3 = [p for p in soup('p')
                        if 'important' in p.get('class', [])]

# And you can combine these to implement more elaborate logic. For example, if you 
# want to find every <span> element that is contained inside a <div> element, you
# could do this:
    # warning, will return the same span multiple times
    # if it sitsd inside multiple divs
    # be more clear if that's the case
    spans_inside_divs = [span
                        for div in soup('div')    # for each <div> on the page
                        for span in div('span')]  # find each <span> inside it

# Just this handful of features will allow us to do quite a lot. If you end up 
# needing to do more-complicated things (or if you're just curious), check the 
# documentation.
#
# Of course, whatever data is important won't typically be labeled as class="important"
# You'll need to carefully inspect the source HTML, reason through your selection 
# logic, and worry about edge cases to make sure your data is correct. Let's look 
# at an example.
#
# Example: O'Reilly Books about Data
# 
# A potential investor in DataSciencester thinks data is just a fad. To prove him
# wrong you decide to examine how many data books O'Reilly has published over time.
# After digging through its website, you find that it has many pages of data books
# ( and videos), reachable through 30-items-at-a-time direcorty pages with URLs like:
# http://shop.oreilly.com/category/browse-subjects/data.do?sortby=publicationDate&page=1
# Unless you want to be a jerk ( and unless you want your scraper to get banned) when
# ever you want to scrape data from a website you should first check to see if it 
# has some sort of access policy. Looking at:
# http://oreilly.com/terms/
# there seems to be nothing prohibiting this project. In order to be good citizens,
# we should also check for a robots.txt file that tells webcrawlers how to behave.
# The important lines in http://shop.oreilly.com/robots.txta are:
# Crawl-delay: 30
# Request- rate: 1/30
# 
# The first tells us that we should wait 30 seconds between requests, the second that 
# we should request only one page every 30 seconds. So basically they're two different
# ways of saying the same thing. (There are other lines that indicate directories not
# to scrap but they don't include our URL, so we're OK there.)
#
# To figure out how to extract the data, let's download one of those pages and feed it
# to Beautiful Soup:

url = http://shop.oreilly.com/category/browse-subjects/data.do?sortby=publicationDate&page=1
soup = BeautifulSoup(requests.get(url).text, 'html5lib')

# If you view the source of the page (in your browser, right-click and select "View
# source" or "View page source" or whatever option looks the most like that), you'll
# see that each book (or video) seems to be uniquely contained in a <td> table cell element
# whose class is thumbtext. Here is (an abridged version of) the relevant HTML for one book:
...
# A good first step is to find all of the td thumbtext tag elements:
tds = soup('td', 'thumbtext')
print len(tds)

# Next we'd like to filter out the videos. ( The would-be investor is only impressed 
# by books.) If we inspect the HTML further, we see that each td contains one or more 
# span elements whose class is pricelabel, and whose text looks like Ebook: or Video:
# or Print:. It appears that the videos contain only one pricelabel, whose text starts
# with VIdeo (after removing leading spaces). This means we can test for videos with:

def is_video(td):
    """It's a video if it has exactly one pricelabel, and if
    the stripped text inside that pricelabel starts with 'Video'"""
    pricelabels = td('span', 'pricelabel')
    return (len(pricelabels) == 1 and
            pricelabels[0].text.strip().startswith("Video"))

print len([td for td in tds if not is_video(td)])

# Now we're ready to start pulling data out of the td elements. It looks like the 
# book title is the text inside the <a> tag inside the <div class="thumbheader">:

title = td.find("div", "thumbheader").a.text

# The author(s) are in the text of the AuthorName <div>. THey are prefaced by a By 
# (which we want to get rid of) and separated by commas (which we want to split out,
# after which we'll need to get rid of spaces):

author_name = td.find('div', 'AuthorName').text
authors = [x.strip() for x in re.sub("^By ", "", author_name).split(",")]

# The ISBN seems to be contained in the link that's in the thumbheader <div>:

isbn_link = td.find("div", "thumbheader").a.get("href")

# re.match captures the part of the regex in parentheses
isbn = re.match("/product/(.*)\.do", isbn_link).group(1)

# And the data is just the contents of the <span class="directorydate">:

date = td.find("span", "directorydate").text.strip()

# Let's put this all together into a function:

def book_info(td):
    """given a BeautifulSoup <td> Tag representing a book,
    extract the book's details and return a dict"""

    title = td.find("div", "thumbheader").a.text
    by_author = td.find('div', 'AuthorName').text
    authors = [x.strip() for x in re.sub("^By ", "", by_author).split(",")]
    isbn_link = td.find("div", "thumbheader").a.get("href")
    isbn = re.match("/product/(.*)\.do", isbn_link).groups()[0]
    date = td.find("span", "directorydate").text.strip()

    return {
        "title" : title,
        "authors" : authors,
        "isbn" : isbn,
        "date" : date
    }

# Amd now we're ready to scrape
from bs4 import BeautifulSoup
import requests
from time import sleep
base_url = "http://shop.oreilly.com/category/browse-subjects/" + \"data.do?sortby=publicationDate&page="

books = []

NUM_PAGES = 31

for page_num in range(1, NUM_PAGES + 1):
    print "souping page", page_num, ",", len(books), " found so far"
    url = base_url + str(page_num)
    soup = BeautifulSoup(requests.get(url).text, 'html5lib')

    for td in soup('td', 'thumbtext'):
        if not is_video(td):
            books.append(book_info(td))
    
    # now to be a good citizen and respect the robots
    sleep(30)

# Now that we've collected the data, we can plot the number of books published 
# each year:

def get_year(book):
    """book["date"] looks like 'November 2014' so we need
    to split on the space and then take the second piece"""
    return int(book["date"].split()[1])

# 2014 is the last complete year of data (when i ran this)
year_counts = Counter(get_year(book) for book in books
                    if get_year(book) <= 2014)

import matplotlib.pyplot as plt 
years = sorted(year_counts)
book_counts = [year_counts[year] for year in years]
plt.plot(years, book_counts)
plt.ylabel("# of data books")
plt.title("Data is Big!")
plt.show()

## Unfortunately, the would be investor looks at the graph and decides that 2013
# was the 'peak data'
#
# Using APIs:
# Many websites and web services provide application programming interfaces (APIs)
# which allow you to excplicitly request data in a structured format. This saves
# you the trouble of having to scrape them!
#
# JSON (and XML):
# Because HTTP is a protocol for transferring text, the data you request through
# a web API needs to be serialized into a string format. OFten this serialization
# uses JavaScript Object Notation (JSON). Javascript objects look quite similar
# to Python Dicts, which makes their string representations easy to interpret:
{ "title" : "Data Science Book",
    "author" : "Joel Grus",
    "publicationYear" : 2014,
    "topics" : ["data", "science", "data science"]}

# We can parse JSON using Python's json module. In particular, we will use its loads
# function, which deserializes a string representing a JSON object into a Python object:

import json
serialized = """{ "title" : "Data Science Book" ,
                    "author" : "Joel Grus",
                    "publicationYear" : 2014,
                    "topics" : [ "data", "science", "data science"] }"""
# parse the JSON to create a Python Dict
deserialized = json.loads(serialized)
if "data science" in deserialized["topics"]:
    print deserialized

# Sometimes an API provider hates you and only provides responses in XML:
#
# You can use beautifulsoup to get data from XML similarly to how we used it to
# get data from HTML; check its documentations for details.
#
# Using an Unauthenticated API:
# Most APIs these days require you to first authenticate yourself in order to use 
# them. While we don't begrudge them this is policy, it creates a lot of extra 
# boilerplate that muddies up our exposition. Accordingly, we'll first take a look 
# at Github's API (http://developer.github.com/v3/), with which you can do some 
# simple things unauthenticated:

import requests, json
endpoint = "https://api.github.com/users/joelgrus/repos"

repos = json.loads(requests.get(endpoint).text)

# At this point repos is a list of Python dicts, each representing a public 
# repository in my GitHub account. ( Feel free to substitute your username and
# get your GitHub repository data instead. You do have a GitHub account right?)
#
# We can use this to figure out which months and days of the week I'm most likely to 
# create a repository. The only issue is that the dates in the response are (Unicode)
# strings:
u'created_at': u'2013-07-05T02:02:28Z'

# Python doesn't come with a great date parser, so we'll need to install one:

from dateutil.parser import parse

dates = [parse(repo["created_at"]) for repo in repos]
month_counts = Counter(date.month for date in dates)
weekday_counts = Counter(date.weekday() for date in dates)

# Similarly, you can get the languages of my last five repositories:

last_5_repositories = sorted(repos,
                            key=lambda r: r["created_at"],
                            reverse=True)[:5]

last_5_languages = [repo["language"]
                    for repo in last_5_repositories]

# Typically we won't be working with APIs at this low "make the requests and parse
# the responses ourselves" level. One of the benefits of using Python is that someone
# has already built a library for pretty much any API you're interested in accessing.
# When they're done well, these libraries can save you a lot of the trouble of figuring
# out the hairier details of API access. (When they're not done well, or when it turns
# out they're based on defunct versions of corresponding APIs, they can cause you 
# enormous headaches.)
#
# Nonetheless, you'll occasionally have to roll your own API-access library (or, more
# likely, debug why someone else's isn't working), so it's good to know some of the 
# details.
#
# Finding APIs:
# If you need data from a specific site, look for a developers or API section of the site
# for details, and try searching the Web for "python__api" to find a library. There is
# a Rotten Tomatoes API for Python. There are multiple Python wrappers for the Klout
# API, for the Yelp API, for the IMDB API, and so on.
#
# If you're looking for lists of APIs that have Python wrappers, two directories are 
# at Python API (http://www.pythonapi.com) and Python for Beginners (http://bit.ly/1L35VOR).
#
# If you want a directory of web APIs more broadly (without Python wrappers necessarily),
# a good resource is Programmable Web (http://www.programmableweb.com), which has a huge
# directory of categorized APIs
#
# And if after all that you can't find what you need, there's always scrapping, the 
# last refuge of the data scientist.
#
# Example: Using the Twitter APIs
# Twitter is a fantastic source of data to work with. You can use it to get real-time
# news. You can use it to measure reactions to current events. You can use it to find
# links related to specific topics. You can use it for pretty much anything you can 
# imagine, just as long as you can get access to its data. And you can get access to\
# its data through its API.
#
# To iteract with the Twitter APIs we'll use the Twython library (http://github.com/ryanmcgrath/twython)
# (pip install twython). There are quite a few Python Twitter libraries out there, 
# but this is the one that I've had the most success working with. You are encouraged
# to explore others as well!
#
# Getting Credentials:
# In order to use Twitter APIs, you need to get some credentials (for which you need
# a twitter account, which you should have anyway so that you can be part of the 
# lively and friendly Twitter #datascience community). Like all instructions that 
# relate to websites that I don't control, these may go obsolete at some point but 
# will hopefully work for a while. (Although they have already changed at least once
# while I was writing this book, so good luck! )
#
# 1. Go to https://apps.twitter.com/
# 2. If you are not signed in, click Sign in and enter your Twitter username and 
# password.
# 3. Click Create New App.
# 4. Give it a name (such as "Data Science") and a description, and put any URL
# as the website (it doesn't matter which one).
# 5. Agree to the Terms of Service and click Create.
# 6. Take note of the consumer key and consumer secret.
# 7. Click "Create my access token."
# 8. Take note of the access token and access token secret (you may have to refresh
# the page).
#
# The consumer key and consumer secret tell Twitter what application is accessing 
# its APIs, while the access token and access token secret tell Twitter who is 
# accessing its APIs. If you have ever used your Twitter account to log in to some
# other site, the "click to authorize" page was generating an access token for that
# site to use to convince Twitter that it was you (or, at least, on your behalf). As
# we don't need this "let anyone log in" functionality, we can get by with the statically 
# generated access token and access token secret.