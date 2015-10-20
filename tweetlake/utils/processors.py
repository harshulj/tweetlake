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

