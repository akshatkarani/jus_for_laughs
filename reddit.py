import os
import csv
import praw
import subprocess


def _init_reddit():
    try:
        return praw.Reddit(user_agent='jokes by akshatkarani',
                           client_id=os.environ['REDDIT_KEY'],
                           client_secret=os.environ['REDDIT_SECRET'],
                           username=os.environ['REDDIT_USERNAME'],
                           password=os.environ['REDDIT_PASSWORD'])
    except KeyError:
        print('Try: "source jokes-env"')


def _get_joke(submission):
    return submission.title + '\n\n' + submission.selftext


def allowed(submission):
    if submission.title == r'r/jokes has a discord and you need to join!':
        return False
    if len(_get_joke(submission)) > 240:
        return False
    return True

def get_subreddits(reddit):
    with open("subreddits.csv", "r") as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            if int(row["enabled"]) == 1:
                subreddit = reddit.subreddit(row["subreddit"])
                yield subreddit

def get_newest():
    reddit = _init_reddit()
    if isinstance(reddit, praw.Reddit):
        subreddits = get_subreddits(reddit)
        
        for subreddit in subreddits:
            for submission in subreddit.hot(limit=5):
                if allowed(submission):
                    yield _get_joke(submission)

    else:
        subprocess.call('source "jokes-env"')
        get_newest()

