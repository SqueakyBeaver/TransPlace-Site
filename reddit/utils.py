from dotenv import load_dotenv
from os import getenv
from datetime import datetime
from django.core.cache import cache
import praw
# import pprint


def get_messages(count=15):
    """
    Get specified messages from the reddit
    :param count: The total amount of messages to get
    :type amount: int
    """

    load_dotenv()

    reddit = praw.Reddit(
        client_id=getenv("REDDIT_CLIENT_ID"),
        client_secret=getenv("REDDIT_CLIENT_SECRET"),
        refresh_token=getenv("REDDIT_REFRESH_TOKEN"),
        user_agent=getenv("REDDIT_USER_AGENT"),
    )

    result = []

    subreddit: praw.reddit.Subreddit = reddit.subreddit("transplace")
    for submission in subreddit.new(limit=count):
        # In case I ever need to figure out
        # all the properties a submission has
        # pprint.pprint(vars(submission))

        if submission.archived:
            print(submission.title, "ARCHIVED")
            continue

        data = {
            "id": submission.id,
            "title": submission.title,
            "content": None,
            "message_type": "User Content",
            "reddit_url": submission.shortlink,
            "created_at": datetime.utcfromtimestamp(submission.created_utc)
        }

        # If the post is an image post
        # We have to do it this way bc PRAW does funny stuff
        try:

            if submission.preview["enabled"]:
                data["file_url"] = submission.url

            if "video" in submission.post_hint:
                data["file_url"] = submission.preview["images"][0]["resolutions"][-1]["url"]

        except BaseException as e:
            pass

        result.append(data)

    # 🙏
    cache.set("posts", result)

    # For convenience
    return result

# get_messages()
