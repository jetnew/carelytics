import praw
import json

with open('config.json', 'r') as f:
    config = json.loads(f.read())

reddit = praw.Reddit(client_id=config['client_id'],
                     client_secret=config['client_secret'],
                     username=config['username'],
                     password=config['password'],
                     user_agent=config['user_agent'])

class Comment:
    def __init__(self, comment):
        self.obj = comment
        self.body = comment.body
        self.score = comment.score
        self.time = comment.created_utc
    def to_list(self):
        return [self.time, self.score, self.body]

import pandas as pd
class Submission:
    def __init__(self, submission):
        self.obj = submission
        submission.comments.replace_more(limit=None)
        self.comments = [Comment(comment) for comment in submission.comments.list()]
        self.title = submission.title
        self.score = submission.score
        self.id = submission.id
        self.url = submission.url
    def get_comments(self):
        return list(self.obj.comments)
    def __repr__(self):
        return f"[{self.id}] {self.title}"
    def to_df(self):
        return pd.DataFrame([c.to_list() for c in self.comments], columns=['time', 'score', 'body'])

def get_subreddit(subreddit, limit=10, reddit=reddit):
    """Get list of submissions within subreddit."""
    return [Submission(sub) for sub in reddit.subreddit(subreddit).hot(limit=limit)]

import string
def remove_punctuations(text):
    """Given string, remove punctuations."""
    table=str.maketrans('','',string.punctuation)
    return text.translate(table)

def get_subreddit_df(subreddit="AsianBeauty", limit=10, reddit=reddit):
    submissions = get_subreddit(subreddit, limit=limit, reddit=reddit)
    dataframes = [submission.to_df() for submission in submissions]
    df = pd.concat(dataframes, ignore_index=True)
    print(f"Created DataFrame of length: {len(df)}")
    df.to_csv(f"reddit_searcher/[{limit}] {subreddit}.csv", index=False)

# get_subreddit_df(subreddit="AsianBeauty", limit=10)
