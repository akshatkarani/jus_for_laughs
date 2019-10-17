import time
from reddit import get_newest
from twitter import post_tweet


def post():
    for tweet in get_newest():
        post_tweet(tweet)


if __name__ == '__main__':
    while True:
        post()
        time.sleep(600)
