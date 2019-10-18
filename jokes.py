import time
from reddit import get_newest
from twitter import post_tweet, post_thread


def post():
    for tweet in get_newest():
        # One-tweet joke
        if len(tweet) <= 280:
            post_tweet(tweet)
        # Threaded (multiple-tweet) joke
        else:
            tweets = []
            tweet_words = tweet.split()
            t = ""
            for word in tweet_words:
                # we check against 279 because we add a space
                if (len(t) + len(word)) <= 279:
                    t += word + " "
                else:
                    tweets.append(t)
                    t = word
            post_thread(tweets)


if __name__ == '__main__':
    while True:
        post()
        time.sleep(600)
