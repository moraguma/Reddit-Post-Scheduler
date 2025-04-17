# Reddit Post Scheduler

This is a script that allows posts to be scheduled and posted at a particular time to Reddit. 

- [x] Post scheduling at specifics times and subreddits
    - [x] Video posts
    - [x] Image posts
    - [x] Gallery posts
    - [x] Gif posts
    - [x] Url posts
    - [x] Regular posts
- [x] Creation of a comment in a just created post

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
post_within_minute_range | Posts that are less than this many minutes away from their posting time will be posted when `main.py` is run | 20
delete_post_from_days_ago | Posts that are schedule for a date more than this many days ago will be deleted from `posts.json` when `main.py` is run | 7

## Example

This example schedules two posts, a title-only post on r/AskReddit at 14:07 of the 12th of July of 2025, and an image post on r/SeveranceAppleTVPlus at 18:47 of the 3rd of June of 2025. With default configurations, these posts will be posted if `main.py` is run within 20 minutes of their posting times. 

```json
{
    "posts": [
        {
            "time_to_post": "2025-07-12T14:07",
            "subreddit": "AskReddit",
            "title": "What's the first game you spent hundreds of hours on?",
            "body": ""
        },
        {
            "time_to_post": "2025-06-03T18:47",
            "subreddit": "SeveranceAppleTVPlus",
            "title": "I am very eagen to post this meme from tumblr",
            "flair": "Meme",
            "image": "media/severance_meme.png",
        }
    ]
}
```

## Automating

I am currently using Windows Scheduler to run main.py every 15 minutes (which you can learn how to do [here](https://www.youtube.com/watch?v=4n2fC97MNac)), but ideally this should probably run on a dedicated server.