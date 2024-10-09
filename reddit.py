import praw
import random
import requests
from dotenv import load_dotenv
import os

load_dotenv()

memes_folder = 'memes'

# Create Reddit instance with your credentials
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent="Shorts Maker"
)

subreddits = ['memes', 'dankmemes', 'ComedyCemetery', 'Animemes', 'MemeEconomy', 'HistoryMemes', 'AdviceAnimals', 'MinecraftMemes', 'formuladank', 'dndmemes']

def download_memes(sub, amount = 1000):
    if(sub == "random" or sub == None):
        sub = random.choice(subreddits)

    if(sub == "all"):
        amount = amount/len(subreddits)
        for sub in subreddits:
            download_memes(sub, amount)
        return

    subreddit = reddit.subreddit(sub)

    for post in subreddit.top(limit=amount):
        if post.url.endswith(('.jpg', '.jpeg', '.png')):
            image_url = post.url
            print(f"Title: {post.title}, URL: {post.url}, Score: {post.score}")
            
            download_image(image_url, f"{memes_folder}/{sub}_{post.id}.jpg")
    
    return

def get_memes(sub, amount):
    all_memes = os.listdir(memes_folder)
    if sub and sub in subreddits:
        memes = [meme for meme in all_memes if meme.startswith(sub)]
    else:
        memes = all_memes

    if len(memes) < amount:
        amount = len(memes)

    random_memes = random.sample(memes, min(amount, 2))

    return [os.path.join(memes_folder, meme) for meme in random_memes]

def download_image(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)
        print(f"Image downloaded: {file_name}")
    else:
        print(f"Failed to download image from {url}")


print(get_memes("all", 2))