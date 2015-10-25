# TweetLake
Tweet Lake is a commandline interface to Twitter Streaming API and big data project that extracts interesting stats out of tweet corpus.

Twitter API is a gold mine for big data lovers. People can do all sort of analysis and find some cool stats using twitter data. Whether it is sentiment analysis on products/topics or demographics. All this is possible on twitter data. I often like playing with machine learning algorithms. And one of the challenges that I face is the availability of data set. Most of the times I am browsing the internet and searching for data. Sometimes I find what I need and sometimes I have to create my own data set. After struggling a lot, I thought may be I can create a flexible tool that can do the job of data collection. So I started building [TweetLake](https://github.com/harshulj/tweetlake). 

**TweetLake (v 0.1.dev1)** is a modular command line tool that makes twitter data collection easier. This is written in Python and makes use of [Tweepy](http://tweepy.org/). It makes the job of data collection simpler. 

##### Installation
You can install TweetLake via pip, but this is not advised as TweetLake is currently in active development. This not very flexible and more over you would want to change the source code as per your convenience.
```
# Installing via pip
$ [sudo] pip install tweetlake
```
The **best way** is to clone the repo.  You can download or clone it from [Github (https://github.com/harshulj/tweetlake)]( https://github.com/harshulj/tweetlake/). Once cloned run the following commands.
```
$ git clone https://github.com/harshulj/tweetlake.git
$ cd tweetlake
$ virtualenv env
$ source env/bin/activate
$ python setup.py develop
```
These commands basically creates a virtual environment and install TweetLake within that environment. This is useful because you can directly edit the source and modify the commands as per your convenience.

##### Usage
Using TweetLake is pretty easy. First step is to create `data/` folder in project root.
Secondly, update `config.py`. Enter your config in tweetlake config
```
$ tl --help
Usage: tl [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  feature  This command takes raw tweets as input and...
  filter   This command either filter tweets based on...
  sample   This command opens a stream to twitter and...
  stats    Use this command to filter on the tweets and...
```
##### Commands
Currently there are 4 commands as mentioned above. 3 of them can be used to collect twitter data.

**First one, *filter*** is for collecting tweets based on keywords.
```
$ tl filter --help
Usage: tl filter [OPTIONS] TWEET_TYPE FILE

  This command either filter tweets based on happy or sad sentiments. OR You
  can also pass the keywords to filter the tweets. User tweet type as
  'custom' to support keywords Either of the 2 will work.

Options:
  --keywords TEXT  Keywords to filter the tweets as CSV
  --place TEXT     Place to filter the public tweets. Make sure this list is
                   less than 25.
  --follow TEXT    List of user ids to filter the public tweets from. Make
                   sure this list is less than 5000 in CSV format
  --help           Show this message and exit.
```

**Second *sample***, is for collecting sample tweets.
```
$ tl  sample --help
Starting Tweet Lake

Usage: tl sample [OPTIONS]

  This command opens a stream to twitter and fetches all the sample tweets.

Options:
  --help  Show this message and exit.
```
**Third one *stats***, prints out number of total tweets collected also the aggregate number of tweets based on language.
```
$ tl stats --help
Starting Tweet Lake

Usage: tl stats [OPTIONS] FILE

  Use this command to filter on the tweets and get the aggregate numbers.

Options:
  --lang TEXT  Aggregate based on the language of the tweet.
  --help       Show this message and exit.

```
##### Data Format
Currently TweetLake supports file for storing tweets. Each tweet is saved as json in a file. This file can be read and processed as per the requirement.

##### Supervisord Support
TweetLake has support for running the commands using supervosord. Currently there are 3 commands that are there in supervisord.conf by default. You can see `supervisor.conf` for more details.

Using supervisor you can collect Twitter's sample data as we ll as you can collect tweets classified as *happy* and *sad*. 

##### Road Ahead
This is just a beginning for TweetLake. I want to convert TweetLake into a big data framework for twitter data. A framework like [scrapy](scrapy.org), which can be extended with easy. Currently I am adding support for Support vector Machine and Naive Bayes Classifier. I'll also add some example commands and algorithms. 

If you have any suggestions or comments please write them below. I would love to get a feedback on what features to add.
