import os
import tweepy
from typing import List

def _init_twitter():
    auth = tweepy.OAuthHandler(os.environ['TWEET_API_KEY'],
                               os.environ['TWEET_API_SECRET'])
    auth.set_access_token(os.environ['TWEET_ACCESS_KEY'],
                          os.environ['TWEET_ACCESS_SECRET'])
    return auth


def _get_api():
    return tweepy.API(_init_twitter())

def post_tweet(tweet: str):
    api = _get_api()
    try:
        api.update_status(tweet)
        print('Successfully Tweeted: ' + tweet)
    except tweepy.error.TweepError as e:
        print(e)

def post_thread(tweets: List[str]):
    """
    Posts a thread of tweets, received as a list
    of strings that are less than 280 characters each.
    """

    api = _get_api()
    try:
        last_status_id = None
        for tweet in tweets:
            if last_status_id is not None:
                status = api.update_status(tweet)
                success_msg = 'Tweeted: %s (%s)'
                info = (tweet, str(status.id))
                print(success_msg % info)
            else:
                status = api.update_status(tweet, last_status_id)
                success_msg = 'Tweeted: %s (%s) as a reply to tweet %s'
                info = (tweet, str(status.id), str(last_status_id))
                print(success_msg % info)
            last_status_id = status.id
    except tweepy.error.TweepError as e:
        print(e)
