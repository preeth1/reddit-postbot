import os
import praw
import tweepy
import inquirer
import webbrowser
from time import sleep
import tempfile
from pathlib import Path
from helpers import generate_thumbnail

from dotenv import load_dotenv
load_dotenv()


UNPOSTED_DIR = '/Volumes/GoogleDrive/My Drive/mystic_village/Marketing/game_gifs/unposted'
POSTED_DIR = '/Volumes/GoogleDrive/My Drive/mystic_village/Marketing/game_gifs/posted'
SUBREDDIT_DETAILS = [
    # {'name': 'test', 'flair_text': None},
    {'name': 'u_auntygames', 'flair_text': None},
    {'name': 'godot', 'flair_text': 'Picture/Video'},
    {'name': 'indiegames', 'flair_text': 'Video'},
    {'name': 'PixelArt', 'flair_text': 'Hand Pixelled'}
]


# FILL OUT CLI PROMPTS
available_files_to_post = []
for filename in os.listdir(UNPOSTED_DIR):
    if Path(filename).suffix == '.mov':
        available_files_to_post.append(filename)
questions = [
    inquirer.List('vid_filename', message="Video to upload", choices=available_files_to_post),
    inquirer.Text('post_title', message="Post title"),
]
answers = inquirer.prompt(questions)
post_title = answers['post_title']
unposted_vid_path = os.path.join(UNPOSTED_DIR, answers['vid_filename'])


# POST TO TWITTER
input('About to post to twitter. Press any key to continue!')

auth = tweepy.OAuth1UserHandler(
    consumer_key=os.environ['TWITTER_API_KEY'],
    consumer_secret=os.environ['TWITTER_API_SECRET'],
    access_token=os.environ['TWITTER_ACCESS_TOKEN'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET']
)
api = tweepy.API(auth)
upload_response = api.media_upload(unposted_vid_path)
hashtags = '\n\n #gamedev #IndieGameDev #pixelart #rpg #godotengine'
api.update_status(status=post_title + hashtags, media_ids=[upload_response.media_id_string])


# POST TO REDDIT
input(f'About to post to the following subs: {[x["name"] for x in SUBREDDIT_DETAILS]}. Press any key to continue! ')

reddit = praw.Reddit(
    client_id=os.environ['REDDIT_CLIENT_ID'],
    client_secret=os.environ['REDDIT_SECRET'],
    password=os.environ['REDDIT_PW'],
    user_agent='localscript:aunty-games-poster:0.0.1 (by /u/auntygames)',
    username="auntygames",
)

for entry in SUBREDDIT_DETAILS:
    sub_name = entry['name']
    print(f'Posting to sub: {sub_name}')
    subreddit = reddit.subreddit(sub_name)
    flair_id = None
    for flair_details in list(subreddit.flair.link_templates.user_selectable()):
        if flair_details['flair_text'] == entry['flair_text']:
            flair_id = flair_details['flair_template_id']

    # Make the outfile a temporary file
    with tempfile.NamedTemporaryFile(suffix='.png') as temp:
        thumbnail = generate_thumbnail(video_path=unposted_vid_path, out_filename=temp.name)
        subreddit.submit_video(
            title=post_title,
            video_path=unposted_vid_path,
            thumbnail_path=temp.name,
            without_websockets=True,
            flair_id=flair_id
        )

user = reddit.redditor('auntygames')
for submission in user.submissions.new():
    if submission.title == post_title:
        submission.reply(body="it's just me working on this project so I would love feedback! \n\n"
                              "✨ demo: https://aunty-games.itch.io/mystic-village")
        print('Adding comment to reddit post')


# OPEN UP POSTS IN CHROME
print('Opening up posts in chrome shortly...')
sleep(2)

browser = webbrowser.get('chrome')
browser.open('https://www.reddit.com/user/auntygames/posts/', new=0, autoraise=True)
browser.open('https://twitter.com/AuntyGames/', new=1, autoraise=True)

# MOVE FILE TO UNPOSTED DIR
posted_vid_path = os.path.join(POSTED_DIR, answers['vid_filename'])
print(f'Moving file to: {posted_vid_path}')
os.rename(unposted_vid_path, posted_vid_path)
