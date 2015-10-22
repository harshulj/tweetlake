import os
import re
import json

class BasicTweetProcessor:
    '''
    Basic Tweet Procesor class extracts basic information from a tweet.
    Such as: id, text, user, created_at, etc.
    '''
    def __init__(self):
        self.allowed_keys = [
                'id', 'text', 'source', 'in_reply_to_status_id', 'entities',
                'in_reply_to_user_id', 'in_reply_to_screen_name', 'user',
                'geo', 'coordinates', 'place', 'contributors', 'is_quote_status',
                'retweet_count', 'favorite_count', 'lang', 'timestamp_ms', 'retweeted_status'
                ]
        self.allowed_user_keys = [
                'id', 'name', 'screen_name', 'location', 'url', 'description',
                'protected', 'verified', 'followers_count', 'friends_count',
                'listed_count', 'favourites_count', 'statuses_count', 'created_at',
                'geo_enabled', 'lang', 'profile_background_color', 'profile_image_url',
                'time_zone'
                ]

    def _clean_tweet(self, tweet):
        data = {}
        for key, value in tweet.iteritems():
            if key == 'user':
                user = {}
                for user_key, user_value in value.iteritems():
                    if user_key in self.allowed_user_keys:
                        user[user_key] = user_value
                data[key] = user
            elif key == 'retweeted_status':
                data[key] = self._clean_tweet(value)
            elif key in self.allowed_keys:
                data[key] = value
        return data

    def process(self, raw):
        raw = json.loads(raw)
        return self._clean_tweet(raw)

    def process_delete(self, raw):
        return json.loads(raw)


class FeatureProcessor:
    '''
    This processor takes raw tweets and convert those tweets into feature words.
    '''

    def __init__(self):
        self.stop_words = []
        self._populate_stop_words()

    def _populate_stop_words(self):
        self.stop_words.append('AT_USER')
        self.stop_words.append('URL')
        current_dir = os.path.dirname(os.path.realpath(__file__))
        fp = open(os.path.join(current_dir, '../resources/stop_words.txt'), 'r')
        line = fp.readline()
        while line:
            word = line.strip()
            self.stop_words.append(word)
            line = fp.readline()
        fp.close()

    def _clean_tweet(self, tweet):
        #Convert to lower case
        tweet = tweet.lower()
        #Convert www.* or https?://* to URL
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
        #Convert @username to AT_USER
        tweet = re.sub('@[^\s]+','AT_USER',tweet)
        #Remove additional white spaces
        tweet = re.sub('[\s]+', ' ', tweet)
        #Replace #word with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        #trim
        tweet = tweet.strip('\'"')
        return tweet

    def _replace_two_or_more(self, s):
        #look for 2 or more repetitions of character and replace with the character itself
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        return pattern.sub(r"\1\1", s)

    def _create_vector(self, tweet):
        featureVector = []
        #split tweet into words
        words = tweet.split()
        for w in words:
            #replace two or more with two occurrences
            w = self._replace_two_or_more(w)
            #strip punctuation
            w = w.strip('\'"?,.')
            #check if the word stats with an alphabet
            val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
            #ignore if it is a stop word
            if(w in self.stop_words or val is None):
                continue
            else:
                featureVector.append(w.lower())
        return featureVector

    def process(self, raw):
        if not isinstance(raw, dict):
            raw = json.loads(raw)
        tweet = self._clean_tweet(raw.get('text', ''))
        if tweet:
            return self._create_vector(tweet)
        else:
            return []


