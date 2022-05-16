import os
import praw
import inquirer
from dotenv import load_dotenv
load_dotenv()


reddit = praw.Reddit(
    client_id=os.environ['REDDIT_CLIENT_ID'],
    client_secret=os.environ['REDDIT_SECRET'],
    password=os.environ['REDDIT_PW'],
    user_agent='localscript:aunty-games-postbot:0.0.1 (by /u/auntygames)',
    username="auntygames",
)
subreddit_name = 'test'
subreddit = reddit.subreddit(subreddit_name)
subreddit.submit_image(
    title='my title',
    image_path='/Users/game/Desktop/weird_img.png',
    without_websockets=True
)
