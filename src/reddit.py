import praw
import keys
from logger import logger


# SUBREDDITS is a dictionary with key as subreddit name and value
# which indicates status. If status is 0 then it won't be used.
SUBREDDITS = {'jokes': 1}


def _init_reddit():
    try:
        return praw.Reddit(user_agent='jokes by akshatkarani',
                           client_id=keys.REDDIT_KEY,
                           client_secret=keys.REDDIT_SECRET,
                           username=keys.REDDIT_USERNAME,
                           password=keys.REDDIT_PASSWORD)
    except KeyError:
        logger.error('Error occurred')
        print('Error occurred')


def _get_post(submission):
    """
    Given a submission returns the post.
    In some posts title is re-written in selftext, this takes care of that.
    """
    post = submission.selftext
    if submission.title.lower() not in post.lower():
        post = submission.title + '\n\n' + post
    return submission.id, post


def _get_subreddits(reddit):
    """
    Returns all the subreddits to use from SUBREDDITS
    """
    for sub, status in SUBREDDITS.items():
        if status == 1:
            yield reddit.subreddit(sub)


def get_newest():
    """
    Returns posts from subreddits
    """
    reddit = _init_reddit()
    if isinstance(reddit, praw.Reddit):
        subreddits = _get_subreddits(reddit)

        for subreddit in subreddits:
            for submission in subreddit.hot(limit=5):
                if not submission.stickied:
                    yield _get_post(submission)
