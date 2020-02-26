import os
import tweepy
import logging


logging.basicConfig(filename='logfile',
                    format='%(asctime)s %(message)s', 
                    filemode='w')

logger=logging.getLogger()
logger.setLevel(logging.DEBUG)


def _init_twitter():
    auth = tweepy.OAuthHandler(os.environ['TWEET_API_KEY'],
                               os.environ['TWEET_API_SECRET'])
    auth.set_access_token(os.environ['TWEET_ACCESS_KEY'],
                          os.environ['TWEET_ACCESS_SECRET'])
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


# Needs some work and some tests
def split_tweet(tweet):
    """
    Split a tweet into multiple tweets if it exceeds the character limit
    """
    tweets = []
    # Try to split at period
    tweet_sentences = tweet.split(".")
    for sentence in tweet_sentences:
        # we check against the 280 character limit
        if (len(sentence)) <= 280:
            tweets.append(sentence)
        else:
            # in case the whole sentence is greater than 280 words
            # we split it progressively
            words = tweet.split()
            t = ""
            for word in words:
                if (len(t) + len(word)) <= 279:
                    t += word + " "
                else:
                    tweets.append(t)
                    t = word


def post(submission_id, tweet):
    # Check if tweet exceeds the character limit of 280
    logger.info('Reddit id: ' + str(submission_id))
    if len(tweet) <= 280:
        post_tweet(tweet)
    else:
        tweets = split_tweet(tweet)
        post_thread(tweets)


if __name__ == '__main__':
    tweets = ['test4', 'test2', 'test3', 'test1']
    for tweet in tweets:
        post_tweet(tweet)
