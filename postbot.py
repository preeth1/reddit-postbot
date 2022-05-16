import os
import praw
import inquirer
from dotenv import load_dotenv
load_dotenv()


UNPOSTED_DIR = '/Volumes/GoogleDrive/My Drive/mystic_village/Marketing/Gifs/unposted'
POSTED_DIR = '/Volumes/GoogleDrive/My Drive/mystic_village/Marketing/Gifs/posted'
SUBREDDIT_NAMES = ['test']

questions = [
    inquirer.List('gif_filename', message="Gif to upload:", choices=os.listdir(UNPOSTED_DIR)),
    inquirer.Text('post_title', message="Post title:"),
]
answers = inquirer.prompt(questions)

reddit = praw.Reddit(
    client_id=os.environ['REDDIT_CLIENT_ID'],
    client_secret=os.environ['REDDIT_SECRET'],
    password=os.environ['REDDIT_PW'],
    user_agent='localscript:aunty-games-postbot:0.0.1 (by /u/auntygames)',
    username="auntygames",
)

input(f'About to post to the following subs: {SUBREDDIT_NAMES}. Press any key to continue')

for sub_name in SUBREDDIT_NAMES:
    print(f'Posting to sub: {sub_name}')
    subreddit = reddit.subreddit(sub_name)
    unposted_gif_path = os.path.join(UNPOSTED_DIR, answers['gif_filename'])
    subreddit.submit_image(
        title=answers['post_title'],
        image_path=unposted_gif_path,
        without_websockets=True
    )
os.rename(unposted_gif_path, os.path.join(POSTED_DIR, answers['gif_filename']))