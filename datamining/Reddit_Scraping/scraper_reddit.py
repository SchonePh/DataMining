import configparser
import praw

config = configparser.ConfigParser()
config.read("Reddit_Scraping/config.properties")
client = config["reddit"]["reddit.client"]
secret = config["reddit"]["reddit.secret"]
user_agent = config["reddit"]["reddit.user_agent"]

print(client, secret, user_agent)

red = praw.Reddit(client_id=client, client_secret=secret, user_agent=user_agent)

hot_posts = red.subreddit("europe").hot(limit=10)
for post in hot_posts:
    print(post.id)
    print(post.title)
    print(post.url)
    print(post.selftext)