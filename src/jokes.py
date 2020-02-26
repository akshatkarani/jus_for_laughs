from reddit import get_newest
from twitter import post


def main():
    """
    Main function
    """
    for submission_id, tweet in get_newest():
        post(submission_id, tweet)


if __name__ == '__main__':
    main()
