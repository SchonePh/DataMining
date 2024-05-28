import configparser
import praw
import pandas as pd

config = configparser.ConfigParser()
config.read("Aufgaben_Reddit/config.properties")
client = config["reddit"]["reddit.client"]
secret = config["reddit"]["reddit.secret"]
user_agent = config["reddit"]["reddit.user_agent"]

red = praw.Reddit(client_id=client, client_secret=secret, user_agent=user_agent)

def get_subreddit(sname, stype, slimit):
    if (stype == "new"):
        posts = red.subreddit(sname).new(limit=slimit)
    elif (stype == "hot"):
        posts = red.subreddit(sname).hot(limit=slimit)
    posts_array = []
    for post in posts:
        posts_array.append([post.id, post.title, post.selftext])
    dm = pd.DataFrame(posts_array, columns=["subreddit_id", "subreddit_title", "subreddit_text"])
    return dm

dataframe = get_subreddit("announcements", "new", 10)

dataframe.to_csv("Aufgaben_Reddit/Aufgabe1_2.csv", index=False)

