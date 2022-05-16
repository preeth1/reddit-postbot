import os
import praw
import inquirer
import webbrowser
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
    user_agent='localscript:aunty-games-poster:0.0.1 (by /u/auntygames)',
    username="auntygames",
)

input(f'About to post to the following subs: {SUBREDDIT_NAMES}. Press any key to continue')

for sub_name in SUBREDDIT_NAMES:
    print(f'Posting to sub: {sub_name}')
    subreddit = reddit.subreddit(sub_name)
    unposted_gif_path = os.path.join(UNPOSTED_DIR, answers['gif_filename'])
    a = subreddit.submit_image(
        title=answers['post_title'],
        image_path=unposted_gif_path,
        timeout=100
    )
posted_gif_path = os.path.join(POSTED_DIR, answers['gif_filename'])
print(f'Moving file to: {posted_gif_path}')
os.rename(unposted_gif_path, posted_gif_path)

user = reddit.redditor('auntygames')
submissions = user.submissions.new(limit=len(SUBREDDIT_NAMES))
browser = webbrowser.get('chrome')
for sub_data in submissions:
    post_url = f'https://www.reddit.com/{sub_data.permalink}'
    print(f'Opening post url: {post_url}')
    browser.open(post_url, new=0, autoraise=True)
