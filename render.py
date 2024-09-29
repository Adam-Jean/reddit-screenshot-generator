#render.py
import os
from playwright.sync_api import sync_playwright, Playwright
import random
import re

# Define the base directory (project directory)
base_directory = os.getcwd()

# Define the path to the assets directory
assets_directory = os.path.join(base_directory, 'assets')

# Define a sub-folder for the generated images
output_folder = os.path.join(base_directory, 'generated_images')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define folder for temp files
temp_files_folder = os.path.join(base_directory, 'temp_files')
os.makedirs(temp_files_folder, exist_ok=True)
if not os.path.exists(temp_files_folder):
    os.makedirs(temp_files_folder)

# Create a function to generate full paths for assets
def get_relative_asset_path(html_file_path, asset_file_name):
    # Find the relative path from the HTML file to the assets directory
    relative_path_to_assets = os.path.relpath(assets_directory, os.path.dirname(html_file_path)).replace('\\', '/')
    
    # Return the full relative path to the asset
    return f"{relative_path_to_assets}/{asset_file_name}"

# HTML Items
nsfw_html = f'''
<img src="{{nsfw_path}}" style="padding-top: 10px; flex-grow: 0; flex-shrink: 0; width: 88px; height: 27px; object-fit: cover;" />
'''

html_imports = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
"""

# HTML template with placeholders
post_template = f"""
<div id="master" style="border: 2px solid #2D3643; font-family: Noto Sans; display: flex; flex-direction: column; justify-content: flex-start; align-items: flex-start; width: 915px; position: relative; gap: 2px; padding: 15px; border-radius: 35px; background: #181d24; border-width: 1px; border-color: #2d3643;">
  <div style="display: flex; justify-content: space-between; align-items: center; align-self: stretch; flex-grow: 0; flex-shrink: 0; position: relative; padding-left: 4px; padding-right: 4px; padding-bottom: 0px;">
    <div style="display: flex; justify-content: flex-start; align-items: center; flex-grow: 0; flex-shrink: 0; position: relative; gap: 9px;">
      <img src={{pfp_directory}} style="flex-grow: 0; flex-shrink: 0; width: 36px; height: 36px; border-radius: 18px; object-fit: cover; transform: scale(1.2);" />
      <div style="line-height: 0; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; flex-grow: 0; flex-shrink: 0; position: relative;">
        <div style="height: 16px; display: flex; justify-content: center; align-items: center; flex-grow: 0; flex-shrink: 0; position: relative; gap: 10px;">
          <p style="flex-grow: 0; flex-shrink: 0; font-size: 16.7px; font-weight: 600; text-align: left; color: #92a1ae;">r/{{subreddit}}</p>
          <div style="display: flex; justify-content: flex-start; align-items: center; flex-grow: 0; flex-shrink: 0; position: relative; gap: 9px;">
            <svg width="4" height="4" viewBox="0 0 4 4" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex-grow: 0; flex-shrink: 0;" preserveAspectRatio="xMidYMid meet">
              <circle cx="2" cy="2" r="2" fill="#506A87"></circle>
            </svg>
            <p style="flex-grow: 0; flex-shrink: 0; font-size: 16px; text-align: left; color: #506a87;">{{time}}</p>
          </div>
        </div>
        <p style="flex-grow: 0; flex-shrink: 0; font-size: 16.7px; font-weight: 380; text-align: left; color: #92a1ae;">{{author}}</p>
      </div>
    </div>
    <div style="flex-grow: 0; flex-shrink: 0; width: 30px; height: 7.5px; position: relative; overflow: hidden; background: url({{more_path}}); background-size: cover; background-repeat: no-repeat; background-position: center;"></div>
  </div>
  {{nsfw_image}}
  <div style="display: flex; justify-content: center; align-items: center; flex-grow: 0; flex-shrink: 0; width: 865px; position: relative; gap: 10px; padding-left: 7px; padding-right: 7px;">
    <p style="flex-grow: 1; width: 851px; font-size: 25.3px; font-weight: 600; text-align: left; color: #bec2c4;">{{prompt}}</p>
  </div>
  <div style="line-height: 0px; display: flex; justify-content: flex-start; align-items: flex-end; flex-grow: 0; flex-shrink: 0; width: 398px; gap: 9px; padding-left: 6px; padding-right: 6px; padding-top: 0px;">
    <div style="display: flex; justify-content: center; align-items: center; flex-grow: 0; flex-shrink: 0; height: auto px; position: relative; gap: 8px; padding-left: 16px; padding-right: 16px; padding-top: 12px; padding-bottom: 12px; border-radius: 30px; background: #1f262e;">
      <div style="flex-grow: 0; flex-shrink: 0; width: 18px; height: 19.98px; position: relative; overflow: hidden; background: url({{upvote_path}}); background-size: cover; background-repeat: no-repeat; background-position: center;"></div>
      <p style="flex-grow: 0; flex-shrink: 0; font-size: 15.1px; font-weight: 600; text-align: left; color: #bbc0c0;">{{upvotes}}</p>
      <div style="flex-grow: 0; flex-shrink: 0; width: 18px; height: 19.98px; position: relative; overflow: hidden; background: url({{downvote_path}}); background-size: cover; background-repeat: no-repeat; background-position: center;"></div>
    </div>
    <div style="display: flex; justify-content: center; align-items: center; flex-grow: 0; flex-shrink: 0; height: auto px; position: relative; gap: 8px; padding-left: 16px; padding-right: 16px; padding-top: 12px; padding-bottom: 12px; border-radius: 30px; background: #1f262e;">
      <div style="flex-grow: 0; flex-shrink: 0; width: 25px; height: 25px; position: relative; overflow: hidden; background: url({{comment_path}}); background-size: cover; background-repeat: no-repeat; background-position: center;"></div>
      <p style="flex-grow: 0; flex-shrink: 0; font-size: 15.1px; font-weight: 600; text-align: left; color: #bbc0c0;">{{comments}}</p>
    </div>
    <div style="display: flex; justify-content: center; align-items: center; flex-grow: 0; flex-shrink: 0; height: auto px; position: relative; gap: 8px; padding-left: 16px; padding-right: 16px; padding-top: 12px; padding-bottom: 12px; border-radius: 30px; background: #1f262e;">
      <div style="flex-grow: 0; flex-shrink: 0; width: 24px; height: 20px; position: relative; overflow: hidden; background: url({{share_path}}); background-size: cover; background-repeat: no-repeat; background-position: center;"></div>
      <p style="flex-grow: 0; flex-shrink: 0; font-size: 15.1px; font-weight: 600; text-align: left; color: #bbc0c0;">Share</p>
    </div>
  </div>
</div>
"""
comment_template = f"""
<div id="master" style="border: 2px solid #2D3643; font-family: Noto Sans; display: flex; flex-direction: column; justify-content: flex-start; align-items: flex-start; width: 915px; position: relative; gap: 2px; padding: 15px; border-radius: 35px; background: #181d24; border-width: 1px; border-color: #2d3643;">
  <div style="display: flex; justify-content: space-between; align-items: center; align-self: stretch; flex-grow: 0; flex-shrink: 0; position: relative; padding-left: 4px; padding-right: 4px; padding-bottom: 10px;">
    <div style="display: flex; justify-content: flex-start; align-items: center; flex-grow: 0; flex-shrink: 0; position: relative; gap: 9px;">
      <img src={{pfp_directory}} style="flex-grow: 0; flex-shrink: 0; width: 36px; height: 36px; border-radius: 18px; object-fit: cover; transform: scale(1.2);" />
      <div style="line-height: 0; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; flex-grow: 0; flex-shrink: 0; position: relative;">
        <div style="height: 16px; display: flex; justify-content: center; align-items: center; flex-grow: 0; flex-shrink: 0; position: relative; gap: 10px;">
          <p style="flex-grow: 0; flex-shrink: 0; font-size: 16.7px; font-weight: 380; text-align: left; color: #92a1ae;">{{comment_author}}</p>
          <div style="display: flex; justify-content: flex-start; align-items: center; flex-grow: 0; flex-shrink: 0; position: relative; gap: 9px;">
            <svg width="4" height="4" viewBox="0 0 4 4" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex-grow: 0; flex-shrink: 0;" preserveAspectRatio="xMidYMid meet">
              <circle cx="2" cy="2" r="2" fill="#506A87"></circle>
            </svg>
            <p style="flex-grow: 0; flex-shrink: 0; font-size: 16px; text-align: left; color: #506a87;">{{time}}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <div style="display: flex; justify-content: center; align-items: center; flex-grow: 0; flex-shrink: 0; width: 865px; position: relative; gap: 10px; padding-left: 7px; padding-right: 7px;">
    <p style="flex-grow: 1; width: 851px; font-size: 25.3px; font-weight: 600; text-align: left; color: #bec2c4;">{{comment_text}}</p>
  </div>
  <div style="line-height: 0px; display: flex; justify-content: flex-start; align-items: center; flex-grow: 0; flex-shrink: 0; width: max-content; gap: 9px; padding-left: 6px; padding-right: 6px; padding-top: 0px;">
    <div style="display: flex; justify-content: center; align-items: center; flex-grow: 0; flex-shrink: 0; height: auto px; position: relative; gap: 8px; padding-left: 16px; padding-right: 16px; padding-top: 12px; padding-bottom: 12px; border-radius: 30px; background: #1f262e;">
      <div style="flex-grow: 0; flex-shrink: 0; width: 18px; height: 19.98px; position: relative; overflow: hidden; background: url({{upvote_path}}); background-size: cover; background-repeat: no-repeat; background-position: center;"></div>
      <p style="flex-grow: 0; flex-shrink: 0; font-size: 15.1px; font-weight: 600; text-align: left; color: #bbc0c0;">{{comment_upvote_count}}</p>
      <div style="flex-grow: 0; flex-shrink: 0; width: 18px; height: 19.98px; position: relative; overflow: hidden; background: url({{downvote_path}}); background-size: cover; background-repeat: no-repeat; background-position: center;"></div>
    </div>
</div>
"""

def render_data(post_data):
    # Create a unique folder for this dataset
    post_name = str(post_data['post_number'])
    unique_folder = os.path.join(base_directory, 'generated_images', post_name)
    
    post_folder = os.path.join(unique_folder, 'post')
    comments_folder = os.path.join(unique_folder, 'comments')
    
    # Create the directories if they don't exist
    os.makedirs(post_folder, exist_ok=True)
    os.makedirs(comments_folder, exist_ok=True)

    
    # Write the post HTML to a temporary file in "temp_files"
    temp_post_file = os.path.join(temp_files_folder, f"post_{str(post_data['id'])}.html")
    
    # Generate HTML for the post
    post_html = post_template.format(
        subreddit = post_data['subreddit'],
        author = f"u/{post_data['author']}" if post_data['author'] else '[deleted]',
        prompt = post_data['content'],
        upvotes = post_data['upvotes'],
        comments = post_data['comments_count'],
        pfp_directory = post_data['pfp'] if isinstance(post_data['pfp'], str) else get_relative_asset_path(temp_post_file, 'pfp.png'),
        time = post_data['date'],
        nsfw_image = nsfw_html.format(nsfw_path = get_relative_asset_path(temp_post_file, 'nsfw.png')) if post_data['nsfw'] else '',   
        
        upvote_path = get_relative_asset_path(temp_post_file,'upvote_red.png' if random.random() < 0.7 else 'upvote.png'),
        comment_path = get_relative_asset_path(temp_post_file,'comment.png'),
        downvote_path = get_relative_asset_path(temp_post_file,'downvote.png'),
        more_path = get_relative_asset_path(temp_post_file,'more.png'),
        share_path = get_relative_asset_path(temp_post_file,'share.png')
    )
    post_html = f"{html_imports}{post_html}" #adding google api fonts
    
    post_file_name = make_valid_filename(f"{post_data['content'][:10]}-post")
    with open(temp_post_file, 'w', encoding='utf-8') as file:
        file.write(post_html)

    # Render the post
    with sync_playwright() as playwright:
        run(playwright, temp_post_file, post_folder, post_file_name)

    # Generate and render comments
    for index, comment in enumerate(post_data['comments']):
        temp_comment_file, comment_file_name = comment_to_file(comment, index + 1, comments_folder)
        with sync_playwright() as playwright:
            run(playwright, temp_comment_file, comments_folder, comment_file_name)

def comment_to_file(comment_data, index, comments_folder):

    # Define temporary comment file
    temp_comment_file = os.path.join(temp_files_folder, f"comment_{str(comment_data['id'])}.html")
    
    
    comment_html = comment_template.format(
        comment_author = comment_data['author'],
        comment_text = comment_data['content'],
        comment_upvote_count = comment_data['upvotes'],
        time = comment_data['date'],
        upvote_path = get_relative_asset_path(temp_comment_file,'upvote_red.png' if random.random() < 0.4 else 'upvote.png'),
        downvote_path = get_relative_asset_path(temp_comment_file,'downvote.png'),
        pfp_directory = comment_data['pfp'] if isinstance(comment_data['pfp'], str) else get_relative_asset_path(temp_comment_file, 'pfp.png') 
    )
    comment_html = f"{html_imports}{comment_html}"

    filename = make_valid_filename(f"{index}-{comment_data['content'][:10]}-comment")
    
    with open(temp_comment_file, 'w', encoding='utf-8') as file:
        file.write(comment_html)

    return temp_comment_file, filename

def run(playwright: Playwright, temp_file, folder_path, filename):
    chromium = playwright.chromium
    browser = chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(f"file://{os.path.abspath(temp_file)}")
    
    # Save screenshot in the specific folder
    page.locator("id=master").screenshot(path=os.path.join(folder_path, f"{filename}.png"), omit_background=True)
    
    browser.close()

def make_valid_filename(filename):
    """
    Takes a filename string and replaces invalid characters (including slashes, newlines)
    for Windows file systems with underscores. Returns a valid filename.
    """
    # Define a pattern for invalid characters in Windows file names
    invalid_characters = r'[<>:"/\\|?*\n\r]'
    
    # Replace invalid characters and newlines with an underscore
    sanitized_filename = re.sub(invalid_characters, '_', filename)
    
    # Trim leading/trailing spaces (which are also invalid in file names)
    sanitized_filename = sanitized_filename.strip()
    
    # Ensure the filename isn't empty after sanitization
    if not sanitized_filename:
        sanitized_filename = "default_filename"
    
    return sanitized_filename