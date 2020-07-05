import json
with open('../config.json', 'r') as f:
    config = json.loads(f.read())

import tweepy
auth = tweepy.OAuthHandler(config['api_key'], config['api_secret_key'])
auth.set_access_token(config['access_token'], config['access_token_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True)

def query_twitter(query, n=10):
    return tweepy.Cursor(api.search,
                         q=query + " -filter:retweets",
                         result_type='recent',
                         include_entities=True,
                         ).items(n)

class Tweet:
    def __init__(self, tweet):
        self.obj = tweet
        self.time = tweet.created_at
        self.id = tweet.id_str
        self.text = tweet.text
    def to_list(self):
        return [self.id, self.time, self.text]

import pandas as pd
def search_twitter(queriesfile="queries.txt", n=10):
    results = []
    with open(queriesfile, 'r') as f:
        for query in f:
            for i, tweet in enumerate(query_twitter(query.strip(), n=n)):
                results.append(Tweet(tweet).to_list())
    return pd.DataFrame(results, columns=['id', 'time', 'text'])

search_twitter("queries.txt", n=10).to_csv("twitter.csv", index=None)

