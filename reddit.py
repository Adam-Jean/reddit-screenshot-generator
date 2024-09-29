#reddit.py

#TODO: Additional filters for post: max char: 230,  no links, no empty/deleted posts


import praw
from praw.models import MoreComments
from datetime import datetime

import os
import json

from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
SECRET_KEY = os.getenv('REDDIT_SECRET_KEY')
USERAGENT = os.getenv('REDDIT_USERAGENT')
USERNAME = os.getenv('REDDIT_USERNAME')
PASSWORD = os.getenv('REDDIT_PASSWORD')

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=SECRET_KEY,
                     user_agent=USERAGENT,
                     )

index_file = 'used_posts_index.json'

def load_used_posts():
    if os.path.exists(index_file):
        with open(index_file, 'r') as file:
            return json.load(file)
    return []

def save_used_posts(index_data):
    with open(index_file, 'w') as file:
        json.dump(index_data, file)

def get_data(sub_name, post_limit=1, comment_limit=2, max_char=300, min_char=45, sort_method='top', time_filter="week"):
    used_posts = load_used_posts()
    post_counter = len(used_posts)
    sub_data = []
    subreddit = reddit.subreddit(sub_name)
    if sort_method =='top':
        sorted_posts = subreddit.top(time_filter=time_filter)
    else:
        sorted_posts = getattr(subreddit, sort_method)()
    
    post_index = 0
    for index, post in enumerate(sorted_posts):
        if post.id not in used_posts and len(post.title) >= min_char:
            post_counter += 1
            post_index += 1
            print(f'SAVING POST {post_index}/{post_limit}')
            post_data = {
                'post_number': post_counter,
                'author': post.author.name if post.author else None,
                'subreddit': sub_name,
                'upvotes': abbreviate_number(post.ups),
                'comments_count': abbreviate_number(post.num_comments),
                'content': post.title,
                'name': post.name,
                'pfp': getattr(post.author, 'icon_img', None),
                'date': time_ago(post.created_utc),
                'nsfw': post.over_18,
                'id': post.id,
                'comments': []
            }            
                     
            if comment_limit > 0:
                post.comment_sort = 'top'
                comments = post.comments.list()
                coment_index = 1
                for comment in comments:
                    if not isinstance(comment, MoreComments) and min_char <= len(comment.body) <= max_char:
                        print(f"SAVING COMMENT {coment_index}/{comment_limit}")
                        comment_data = {
                            'author': comment.author.name if comment.author else '[deleted]',
                            'upvotes': abbreviate_number(comment.score),
                            'content': comment.body,
                            'date': time_ago(comment.created_utc),
                            'pfp': getattr(comment.author, 'icon_img', None),
                            'id': comment.id
                        }
                        post_data['comments'].append(comment_data)
                        if len(post_data['comments']) == comment_limit:
                            break
                        coment_index += 1
            used_posts.append(post.id)
            sub_data.append(post_data)
            save_used_posts(used_posts)

            if len(sub_data) == post_limit:  # Stop once we have enough valid posts
                break

    return sub_data

def abbreviate_number(n):
    if n >= 1_000_000:
        return f"{n // 1_000_000}M" if n % 1_000_000 < 100_000 else f"{round(n / 1_000_000)}M"
    elif n >= 100_000:
        return f"{n // 1_000}K"
    elif n >= 10_000:
        return f"{n // 1_000}K"
    elif n >= 1_000:
        return f"{round(n / 1_000, 1)}K"
    else:
        return str(n)

def time_ago(unix_time):
    # Convert Unix time (seconds since epoch) to a naive datetime object (UTC)
    utc_time = datetime.utcfromtimestamp(unix_time)
    
    # Get current time in UTC
    now = datetime.utcnow()
    
    # Calculate the time difference
    diff = now - utc_time
    
    # Break down the difference into components
    seconds = diff.total_seconds()
    
    # Convert to minutes, hours, days, weeks, months, and years
    intervals = [
        ('yr', 60 * 60 * 24 * 365),  # years
        ('mo', 60 * 60 * 24 * 30),   # months
        ('wk', 60 * 60 * 24 * 7),    # weeks
        ('day', 60 * 60 * 24),       # days
        ('hr', 60 * 60),             # hours
        ('min', 60),                 # minutes
    ]
    
    # Find the appropriate time unit
    for unit, seconds_in_unit in intervals:
        if seconds >= seconds_in_unit:
            count = int(seconds // seconds_in_unit)
            return f"{count} {unit}{'s' if count > 1 else ''} ago"
    
    return "just now"  # if the time difference is less than a minute


