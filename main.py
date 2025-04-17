import praw
from praw.models import Subreddit, Submission
import json
import platform
from dateutil import parser
from datetime import datetime
import logging


APP_VERSION = "v0.1"
AUTO_POST_TIME_TOLERANCE = 30.0
SCHEDULED_POST_DELETE_TIME = 7


logger = logging.getLogger(__name__)
logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


def post(reddit: praw.Reddit, post_data: dict) -> None:
    """
    Given a post_data, posts the given post. post_data should be:

    {
        "subreddit": <subreddit to post in without the r/>,
        "title": <post title>,
        "flair": <name of flair if post has flair>
        "comment": <comment to add to the post>,
        "video": <video path for video posts>,
        "image": <image path for image posts. Can also be a gif>,
        "gallery": <list of image paths for gallery posts>
        "url": <url for url posts>
        "body": <body of post for simple posts>
    }

    Note that data types above take precedent from ones below. This means that if video is provided all arguments
    below will be ignored and so forth
    """
    # Gets subreddit
    subreddit: Subreddit = reddit.subreddit(post_data["subreddit"])

    # Gets flair
    flair_id = None
    if "flair" in post_data:
        choices = list(subreddit.flair.link_templates.user_selectable())
        flair_id = next(x for x in choices if x["flair_text"] == post_data["flair"])["flair_template_id"]

    # Submits post
    kwargs = {"title": post_data["title"], "flair_id": flair_id}
    if "video" in post_data:
        submission: Submission = subreddit.submit_video(video_path=post_data["video"], timeout=30, **kwargs)
    elif "image" in post_data:
        submission: Submission = subreddit.submit_image(image_path=post_data["image"], timeout=30, **kwargs)
    elif "gallery" in post_data:
        images = []
        for image_path in post_data["gallery"]:
            images.append({"image_path": image_path})
        submission: Submission = subreddit.submit_gallery(images=images, **kwargs)
    elif "url" in post_data:
        submission: Submission = subreddit.submit(url=post_data["url"], **kwargs)
    else:
        submission: Submission = subreddit.submit(selftext=post_data["body"], **kwargs)

    # Leaves comment
    if "comment" in post_data:
        submission.reply(post_data["comment"])


def delete_old_posts(posts: dict, delete_days_ago: int) -> None:
    """
    Deletes from posts all posts scheduled for a day more than delete_days_ago. Returns whether or not an operation was performed
    """
    deleted = False

    now = datetime.now()
    idx = 0
    while idx < len(posts["posts"]):
        scheduled_time = parser.parse(posts["posts"][idx]["time_to_post"])
        elapsed_time = now - scheduled_time
        if elapsed_time.days > delete_days_ago:
            posts["posts"].pop(idx)
            deleted = True
            logger.info(f"Deleted old post \'{posts['posts'][idx]['title'] if 'title' in posts['posts'][idx] else 'UNNAMED'}\' on r/{posts['subreddit'] if 'subreddit' in posts['posts'][idx] else 'UNKNOWN'}")
        else:
            idx += 1
    return deleted


def post_scheduled(posts: dict, minute_range: int, reddit: praw.Reddit) -> None:
    """
    Posts all posts that are scheduled within the given minute range. Returns whether or not at least one post was posted
    """
    posted = False

    now = datetime.now()
    for post_data in posts["posts"]:
        if "posted" in post_data and post_data["posted"]:
            continue

        scheduled_time = parser.parse(post_data["time_to_post"])
        elapsed_time = now - scheduled_time
        if abs(elapsed_time.total_seconds()) / 60.0 < minute_range:
            try:
                post(reddit, post_data)
                post_data["posted"] = True
                posted = True
                logger.info(f"Posted \'{post_data['title']}\' on r/{post_data['subreddit']}")
            except Exception as e:
                logger.exception(e)
    return posted


def json_as_dict(path: str) -> dict:
    with open(path) as json_file:
        return json.load(json_file)


if __name__ == '__main__':
    credentials = json_as_dict("credentials.json")
    posts = json_as_dict("posts.json")
    options = json_as_dict("options.json")

    reddit = praw.Reddit(
        client_id=credentials["client_id"],
        client_secret=credentials["client_secret"],
        password=credentials["password"],
        user_agent=f"{platform.system()}:RedditPostScheduler:{APP_VERSION} (by u/guambe) (being run by u/{credentials['username']})",
        username=credentials["username"]
    )

    changed = delete_old_posts(posts, options["delete_post_from_days_ago"])
    changed = changed or post_scheduled(posts, options["post_within_minute_range"], reddit)

    # Saves posts.json
    with open("posts.json", "w") as json_file:
        json_file.write(json.dumps(posts, indent=4, separators=(',', ': ')))