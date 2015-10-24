from setuptools import setup

setup(
    name='Tweet Lake',
    version='0.1.dev1',
    description='Tweet Lake is a commandline interface to Twitter Streaming API and big data project that extracts interesting stats out of tweet corpus.',
    url='https://harshulja.in/projects/tweet-lake/',
    download_url='https://github.com/harshulj/tweetlake/tarball/0.1.dev1',
    author='Harshul Jain',
    author_email='harshulj@gmail.com',
    license='MIT',
    keywords='twitter, streaming, api, tweepy, commandline',
    packages=[
        'tweetlake',
        'tweetlake.console',
        'tweetlake.stream',
        'tweetlake.utils'
    ],
    install_requires=[
        'click',
        'tweepy',
        'supervisor'
    ],
    entry_points={
        'console_scripts': [
            'tl = tweetlake.console.tl:run'
        ]
    }
)
