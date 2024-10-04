# Reddit Post Screenshot Generator

![Alt Text](https://github.com/Adam-Jean/markdown/blob/main/ReadMe_Banner.png)

This project automates the extraction of Reddit posts and renders them into custom image templates, making it easier to generate content for platforms like TikTok and Instagram. Using Python, PRAW API, and Playwright, this tool captures real-time Reddit data and converts it into proffessional and shareable images.

## 🚀 Features

* **Real-time Reddit Data**: Fetches Reddit posts and comments dynamically using the PRAW API
* **Customizable Templates**: HTML templates designed in Figma, mimic the look of real reddit posts and can be easily modified via Python string literals
* **Headless Image Generation**: Renders HTML to images using Playwright and does not require a display.
* **Content Creation Ready**: Organizes image outputs into organized directories, pairing submissions with associated comments.
* **Configurable Parameters**: Allows users to define parameters such as the number of posts and comments generated, minimum post length, target subreddit, and sort type (e.g., hot, top, rising).

  ## Output Examples

* Generated Post Examples:
  ![Reddit Post](https://github.com/Adam-Jean/markdown/blob/main/What%20are%20s-post.png)
  ![Reddit Post](https://github.com/Adam-Jean/markdown/blob/main/What%20disea-post.png)
  

* Generated Comment Examples:
  ![Reddit Post](https://github.com/Adam-Jean/markdown/blob/main/1-Don%E2%80%99t%20quit-comment.png)
  ![Reddit Post](https://github.com/Adam-Jean/markdown/blob/main/6-My%20daughte-comment.png)
  

## 🛠️ Tech Stack

* **Python**: Core language used for scripting and automation
* **PRAW API**: Interface for interacting with Reddit, retrieving posts and filtering data (requires api key and Reddit login info)
* **Playwright**: Headless browser used to convert HTML into images
* **HTML/CSS**: Custom templates dynamically populated with Reddit post data
* **Figma**: Design tool used to create the visual structure of the image templates

## 📂 Project Structure

```
├── reddit_post_generator
│   ├── assets
│   │   └── (Template images, icons, etc.)
│   ├── main.py      # Loads user input to pull data and render images
│   ├── reddit.py    # Fetches Reddit data via PRAW API
│   ├── render.py    # Populates HTML templates and renders images using Playwright
│   ├── config.json  # Stores user defined arguments
│   ├── .env         # Where api key and sensitive reddit info is stored
│   └── generated_images     # Directory structure for generated images
│       └── {Submission Number}
│           ├── post
│               └── (post.png)
│           └── comments
│               ├── (comment1.png)
│               └── (comment2.png)
│               ...
```

## ⚙️ Setup & Installation

1. **Clone the repository**:
```bash
git clone https://github.com/Adam-Jean/reddit-post-screenshot-generator.git
```

2. **Install the required dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up your Reddit API credentials**:
   * Obtain Reddit API Key and credentials [here](https://www.reddit.com/prefs/apps/). Or see online tutorial [here](https://rymur.github.io/setup):
   * Add your credentials to an `.env` file:
```
REDDIT_CLIENT_ID=your-reddit-client-id
REDDIT_SECRET_KEY=your-reddit-api-key
REDDIT_USERAGENT=your-useragent-name
REDDIT_USERNAME=your-reddit-username
REDDIT_PASSWORD=your-reddit-password
```

4. **Run the script**:
```bash
python main.py
```

## 💡 Usage

* Modify the filtering criteria in `configs.josn` to define which Reddit posts you want to capture (e.g., by subreddit, keyword, etc.)
* The generated images will be saved in the `generated_images` directory (created upon execution), organized by post and comments
