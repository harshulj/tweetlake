import click
import tweepy

from tweetlake import config
from tweetlake.sinks import FileSink
from tweetlake.stream.stream_listeners import SListener

@click.group()
def run():
    click.echo(click.style('Starting Tweet Lake\n', fg='black', bg='green'))

@run.command()
@click.option('--filter', default=False, help='Use this option to filter tweets based on place, user ids and keywords using twitter stream')
@click.option('--place', default=[], help='Place to filter the public tweets. Make sure this list is less than 25.')
@click.option('--follow', default=[], help='List of user ids to filter the public tweets from. Make sure this list is less than 5000')
@click.option('--track', default=[], help='Keywords to filter the public tweets on. Make sure this list is less than 400 words.')
def stream(filter, place, follow, track):
    '''
    This command opens a stream to twitter and fetches all the sample tweets.
    You can use filter switch to specify filter words on which filtering of stream should be done.
    '''
    if filter:
        click.echo(click.style('Opening Stream to Twitter with following options....\n', fg='green'))
        click.echo(click.style('Place: %s\n' % place))
        click.echo(click.style('Follow: %s\n' % follow))
        click.echo(click.style('Track: %s\n' % track))
    else:
        click.echo(click.style('Opening Stream to Twitter to collect sample tweets\n', fg='green'))

    data_file = 'data/test.json'
    file_sink = FileSink(data_file)

    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    api = tweepy.API(auth)
    listener = SListener(api, file_sink)
    stream = tweepy.Stream(auth, listener)

    while True:
        try:
            if not filter:
                stream.sample()
            else:
                stream.filter()
        except Exception as e:
            click.echo(click.style("error!: %s" % e, bg='red', fg='white'))
            stream.disconnect()
            click.echo(click.style("Starting Streaming again.", fg='green'))

