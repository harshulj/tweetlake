import json
import click
import tweepy
import datetime

from tweetlake import config
from tweetlake.utils import filters
from tweetlake.utils.sinks import FileSink
from tweetlake.utils.processors import BasicTweetProcessor, FeatureProcessor
from tweetlake.stream.stream_listeners import SListener

@click.group()
def run():
    click.echo(click.style('Starting Tweet Lake\n', fg='black', bg='green'))

@run.command()
def sample():
    '''
    This command opens a stream to twitter and fetches all the sample tweets.
    '''
    click.echo(click.style('Opening Stream to Twitter to collect sample tweets\n', fg='green'))

    now = datetime.datetime.now()
    data_file = 'data/test-%s.json' % now.strftime('%Y-%m-%d')
    tweet_processor = BasicTweetProcessor()
    file_sink = FileSink(data_file, tweet_processor)

    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    api = tweepy.API(auth)
    listener = SListener(api, file_sink)
    stream = tweepy.Stream(auth, listener)

    while True:
        try:
            stream.sample()
        except Exception as e:
            click.echo(click.style("error!: %s" % e, bg='red', fg='white'))
            stream.disconnect()
            click.echo(click.style("Starting Streaming again.", fg='green'))

@run.command()
@click.option('--tweets', type=click.File('rb'), help='File to read the tweets from')
def feature(tweets):
    '''
    This command takes raw tweets as input and converts them into features.
    '''
    featureList = []
    for line in tweets:
        feature_processor = FeatureProcessor()
        raw = json.loads(line)
        if raw.get('text') and raw.get('lang') == 'en':
            features = feature_processor.process(raw)
            if features:
                featureList.extend(features)
    list(set(featureList))
    print len(featureList)


@run.command()
@click.argument('tweet_type', nargs=1)
@click.argument('file', type=click.File('ab'))
@click.option('--keywords', nargs=1, type=unicode, help='Keywords to filter the tweets as CSV')
@click.option('--place', default=[], help='Place to filter the public tweets. Make sure this list is less than 25.')
@click.option('--follow', nargs=1, type=unicode, help='List of user ids to filter the public tweets from. Make sure this list is less than 5000 in CSV format')
def filter(tweet_type, file, keywords, place, follow):
    '''
    This command either filter tweets based on happy or sad sentiments.
    OR You can also pass the keywords to filter the tweets.
    User tweet type as 'custom' to support keywords Either of the 2 will work.
    '''
    click.echo(click.style('Filtering tweets', fg='green'))
    if tweet_type == 'happy':
        keywords = filters.happy
    elif tweet_type == 'sad':
        keywords = filters.sad + filters.angry
    elif tweet_type == 'custom':
        keywords = keywords.split(',')
    else:
        raise Exception('Not Supported Tweet Type')

    click.echo(click.style('Filtering for: %s' % str(keywords)))

    tweet_processor = BasicTweetProcessor()
    file_sink = FileSink(file, tweet_processor)

    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    api = tweepy.API(auth)
    listener = SListener(api, file_sink)
    stream = tweepy.Stream(auth, listener)

    while True:
        try:
            stream.filter(track=keywords)
        except Exception as e:
            click.echo(click.style("error!: %s" % e, bg='red', fg='white'))
            stream.disconnect()
            click.echo(click.style("Starting Streaming again.", fg='green'))

@run.command()
@click.argument('file', type=click.File('rb'))
@click.option('--lang', default='en', help='Aggregate based on the language of the tweet.')
def stats(file, lang):
    '''
    Use this command to filter on the tweets and get the aggregate numbers.
    '''
    click.echo(click.style('Collecting stats from: %s' % file.name, fg='green'))
    total_count = 0
    lang_count = 0
    error_count = 0
    for line in file:
        try:
            total_count += 1
            tweet = json.loads(line)
            if tweet.get('lang') == lang:
                lang_count += 1
        except Exception as e:
            click.echo(click.style("%s : " % e, fg='red') + line)
            error_count += 1
    print "Unable to decode %d tweets" % error_count
    print "Total tweets: %d" % total_count
    print "Total tweets with lang %s: %d" % (lang, lang_count)

