import re
import tweepy
import keys
from logger import logger


def _init_twitter():
    auth = tweepy.OAuthHandler(keys.TWEET_API_KEY,
                               keys.TWEET_API_SECRET)
    auth.set_access_token(keys.TWEET_ACCESS_KEY,
                          keys.TWEET_ACCESS_SECRET)
    return auth


def _get_api():
    return tweepy.API(_init_twitter())


def post_tweet(tweet: str, last_status_id=None):
    """
    Posts a tweet
    """
    api = _get_api()
    try:
        status = api.update_status(tweet, last_status_id)
        logger.info('Tweet id: ' + str(status.id))
        return status.id
    except tweepy.error.TweepError as e:
        logger.error(e)


def post_thread(tweets: list):
    """
    Posts a thread of tweets, received as a list
    of strings that are less than 280 characters each.
    """
    last_status_id = None
    for tweet in tweets:
        last_status_id = post_tweet(tweet, last_status_id)


def check(tweets):
    for tweet in tweets:
        if len(tweet) > 280:
            return False
    return True

def split_tweet(tweet):
    """
    Split a tweet into multiple tweets if it exceeds the character limit
    """
    # Try spliting based on new line
    tweets = tweet.split('\n')
    if not check(tweets):
        # Try spliting based on period
        tweets = re.split('[\n.]', tweet)
        tweets = [t + '. ' for t in tweets if t]
    if check(tweets):
        tweets = [t for t in tweets if t]
        new = []
        curr_tweet = ''
        for i, tweet in enumerate(tweets):
            if len(tweet) + len(curr_tweet) > 280:
                new.append(curr_tweet)
                curr_tweet = tweet
            else:
                curr_tweet += tweet
        return new + [curr_tweet]
    return False

def post(submission_id, tweet):
    # Check if tweet exceeds the character limit of 280
    logger.info('Reddit id: ' + str(submission_id))
    if len(tweet) <= 280:
        post_tweet(tweet)
    else:
        tweets = split_tweet(tweet)
        if not tweets:
            return
        post_thread(tweets)
