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
            post_thread(tweets)

if __name__ == '__main__':
    while True:
        post()
        time.sleep(600)
