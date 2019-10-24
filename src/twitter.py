import os
import tweepy


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
