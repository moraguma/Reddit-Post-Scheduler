import praw
from praw.models import InlineGif, InlineImage, InlineVideo, Subreddit, Submission
import json
import platform


APP_VERSION = "v0.1"
AUTO_POST_TIME_TOLERANCE = 30.0
SCHEDULED_POST_DELETE_TIME = 7


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

    print(f"Created post {post_data['title']}")


if __name__ == '__main__':
    with open("credentials.json") as json_file:
        credentials = json.load(json_file)
    reddit = praw.Reddit(
        client_id=credentials["client_id"],
        client_secret=credentials["client_secret"],
        password=credentials["password"],
        user_agent=f"{platform.system()}:RedditPostScheduler:{APP_VERSION} (by u/guambe) (being run by u/{credentials['username']})",
        username=credentials["username"]
    )
    