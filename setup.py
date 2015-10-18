from setuptools import setup

setup(
    name='Tweet Lake',
    version='0.1',
    description='Tweet Lake is a big data project that extracts interesting stats out of tweet corpus.',
    url='https://harshulja.in/projects/tweet-lake/',
    author='Harshul Jain',
    license='MIT',
    packages=[
        'tweetlake',
        'tweetlake.console',
        'tweetlake.stream'
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
