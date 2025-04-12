import os
import requests
import praw

reddit = praw.Reddit(
    client_id="myr1YjlOXuvnOXxz3cchRg",
    client_secret="_w56YVG9AMitCYE78jb8xE9zcmmpiA",
    user_agent="Agent_scrap"
)
subreddit_name = 'CombatFootage'
post_limit = 10
os.makedirs("scrapped", exist_ok=True)

def pobierz_video(url, filename):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Pobrano: {filename}")
        else:
            print(f" Błąd pobierania: {url}")
    except Exception as e:
        print(f"Wyjątek: {e}")
subreddit = reddit.subreddit(subreddit_name)

for post in subreddit.hot(limit=post_limit):
    if post.is_video and post.media:
        try:
            video_url = post.media['reddit_video']['fallback_url']
            video_id = post.id
            filename = f"scrapped/{subreddit_name}_{video_id}.mp4"
            pobierz_video(video_url, filename)
        except Exception as e:
            print(f" Nie udało się pobrać: {post.title} | {e}")
    else:
        print(f"⏭ Pominięto (brak video): {post.title}")