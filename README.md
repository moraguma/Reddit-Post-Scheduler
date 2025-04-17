# Reddit Post Scheduler

This is a script that allows posts to be scheduled and posted at a particular time to Reddit. 

- [ ] Post scheduling at specifics times and subreddits
    - [x] Video posts
    - [x] Image posts
    - [x] Gallery posts
    - [x] Gif posts
    - [x] Url posts
    - [x] Regular posts
- [ ] Creation of a comment in a just created post

## Setup

Create a [Reddit app](https://www.reddit.com/prefs/apps) for Reddit Auto Poster. Set it up as a **script**.

| Field | Input |
---|---
about url | https://github.com/moraguma/Reddit-Post-Scheduler
redirect uri | http://localhost

Then, create a file called `credentials.json` in the same folder as main.py with the following content

```json
{
    "username": "YOUR REDDIT USERNAME",
    "password": "YOUR REDDIT PASSWORD",
    "client_id": "YOUR APP'S CLIENT ID",
    "client_secret": "YOUR APP'S CLIENT SECRET"
}
```

## Usage

This should work on all versions of Python that support praw, but not that the project was only tested on Windows running Python 3.10.11

First, you will need to install [PRAW](https://praw.readthedocs.io/en/stable/). You do this with pip using the following command or you can read about more option on the [docs](https://praw.readthedocs.io/en/stable/getting_started/installation.html)

```bash
pip install praw
```

The script `main.py` will read scheduled post information from `posts.json` and will submit posts that are scheduled for a nearby time. `posts.json` follows the structure showcased below. Note that a post can only be of one type. In this application, the order of precedence goes video, image, gallery, url, and simple posts. This means that, for instance, if "image" is set, the program will completely ignore any information in the "url" or "gallery" fields

```json
{
    "posts": [
        {
            "time_to_post": "<Post time in ISO 8601 format - YYYY-MM-DDThh:mm>",
            "subreddit": "<subreddit to post in without the r/>",
            "title": "<post title>",
            "flair": "<name of flair if post has flair>",
            "comment": "<comment to add to the post>",
            "video": "<video path for video posts>",
            "image": "<image path for image posts. Can also be a gif>",
            "gallery": "<list of image paths for gallery posts>",
            "url": "<url for url posts>",
            "body": "<body of post for simple posts>"
        },
        ... MORE POSTS
    ]
}
```

With your posts scheduled, you can run `main.py` with the command below. This will go over your posts, deleting the old ones, and posting and internally tagging as posted the ones scheduled for a nearby time.

```bash
python main.py
```

The file `options.json` can be modified to adjust the functionality of the program. The table below displays the available options.

Option | Description | Default value
---|---|---
post_within_minute_range | Posts that are less than this many minutes away from their posting time will be posted when `main.py` is run | 30
delete_post_from_days_ago | Posts that are schedule for a date more than this many days ago will be deleted from `posts.json` when `main.py` is run | 7

