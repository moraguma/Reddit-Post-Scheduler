# Reddit Post Scheduler

This is a script that allows posts to be scheduled and posted at a particular time to Reddit. 

- [ ] Post scheduling at specifics times and subreddits
    - [ ] Video posts
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
