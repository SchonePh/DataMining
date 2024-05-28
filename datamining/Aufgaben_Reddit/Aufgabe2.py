import configparser
import praw
import pandas as pd
from datetime import datetime

config = configparser.ConfigParser()
config.read("Aufgaben_Reddit/config.properties")
client = config["reddit"]["reddit.client"]
secret = config["reddit"]["reddit.secret"]
user_agent = config["reddit"]["reddit.user_agent"]

red = praw.Reddit(client_id=client, client_secret=secret, user_agent=user_agent)

def get_comment(sname, stype, slimit):
    if (stype == "new"):
        posts = red.subreddit(sname).new(limit=slimit)
    elif (stype == "hot"):
        posts = red.subreddit(sname).hot(limit=slimit)
    comments_array = []
    for post in posts:
        submission = red.submission(id=post.id)
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            submission_date = datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S')
            comment_date = datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
            
            comments_array.append([post.id, submission_date, comment.id, comment.body, comment.score, comment.author, comment_date])
    dm = pd.DataFrame(comments_array, columns=["subreddit_id", "s_date", "comment_id", "c_text", "c_upvotes", "c_author", "c_date"])
    return dm

dataframe = get_comment("hacking", "hot", 2)

dataframe.to_csv("Aufgaben_Reddit/Aufgabe2.csv", index=False)

