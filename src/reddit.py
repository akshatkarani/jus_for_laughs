import os
import praw


# SUBREDDITS is a dictionary with key as subreddit name and value
# which indicates status. If status is 0 then it won't be used.
SUBREDDITS = {'jokes': 1}


def _init_reddit():
    try:
        return praw.Reddit(user_agent='jokes by akshatkarani',
                           client_id=os.environ['REDDIT_KEY'],
                           client_secret=os.environ['REDDIT_SECRET'],
                           username=os.environ['REDDIT_USERNAME'],
                           password=os.environ['REDDIT_PASSWORD'])
    except KeyError:
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


def allowed(submission):
    """
    Return False if a submission is not allowed otherwise returns True
    Needed because some subreddits have pinned posts.
    """
    # Remove the pinned post from r/jokes
    if submission.title == r'r/jokes has a discord and you need to join!':
        return False
    return True


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
            for submission in subreddit.hot(limit=50):
                if allowed(submission):
                    yield _get_post(submission)
