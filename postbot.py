import os
import praw
import inquirer
import webbrowser
from time import sleep
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()


UNPOSTED_DIR = '/Volumes/GoogleDrive/My Drive/mystic_village/Marketing/game_gifs/unposted'
POSTED_DIR = '/Volumes/GoogleDrive/My Drive/mystic_village/Marketing/game_gifs/posted'
SUBREDDIT_NAMES = ['u_auntygames', 'godot', 'indiegames', 'PixelArt']

available_files_to_post = []
for filename in os.listdir(UNPOSTED_DIR):
    if Path(filename).suffix == '.gif':
        available_files_to_post.append(filename)
questions = [
    inquirer.List('gif_filename', message="Gif to upload", choices=available_files_to_post),
    inquirer.Text('post_title', message="Post title"),
]
answers = inquirer.prompt(questions)

reddit = praw.Reddit(
    client_id=os.environ['REDDIT_CLIENT_ID'],
    client_secret=os.environ['REDDIT_SECRET'],
    password=os.environ['REDDIT_PW'],
    user_agent='localscript:aunty-games-poster:0.0.1 (by /u/auntygames)',
    username="auntygames",
)

input(f'About to post to the following subs: {SUBREDDIT_NAMES}. Press any key to continue! ')

for sub_name in SUBREDDIT_NAMES:
    print(f'Posting to sub: {sub_name}')
    subreddit = reddit.subreddit(sub_name)
    unposted_gif_path = os.path.join(UNPOSTED_DIR, answers['gif_filename'])
    subreddit.submit_image(
        title=answers['post_title'],
        image_path=unposted_gif_path,
        without_websockets=True
    )
posted_gif_path = os.path.join(POSTED_DIR, answers['gif_filename'])
print(f'Moving file to: {posted_gif_path}')
os.rename(unposted_gif_path, posted_gif_path)

print('Opening up posts in chrome shortly...')
sleep(5)

browser = webbrowser.get('chrome')
browser.open('https://www.reddit.com/user/auntygames/posts/', new=0, autoraise=True)

user = reddit.redditor('auntygames')
for submission in user.submissions.new():
    if submission.title == answers['post_title']:
        submission.reply(body="it's just me working on this project so I would love feedback! \n\n"
                              "✨ demo: https://aunty-games.itch.io/mystic-village")
