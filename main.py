# main.py
from reddit import get_data
from render import render_data
import logging
import json


logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def load_config():
    with open('config.json') as f:
        return json.load(f)


# sort method options: top, rising, hot
def main():
    try:
        # Fetch data from reddit
        config = load_config()
        subreddit_name = config["subreddit_name"]
        sort_method = config["sort_method"]
        time_frame = config["time_frame"]
        post_limit = config["post_limit"]
        comment_limit = config["comment_limit"]
        max_char = config["max_char"]
        min_char = config["min_char"]

        posts = get_data(subreddit_name, post_limit=post_limit, comment_limit=comment_limit, max_char=max_char, min_char=min_char, sort_method=sort_method, time_filter=time_frame)

        # For each post, generate an image
        for post in posts:
            try:
                render_data(post)
                print(f"Generated image for post: {post['name']}")
            except Exception as e:
                print(f"Failed to generate image for post: {post['name']} - Error: {e}")
    except Exception as e:
        print(f"Error fetching data from Reddit: {e}")

if __name__ == "__main__":
    main()
    print("COMPLETE")