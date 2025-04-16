import praw
from datetime import datetime
import pandas as pd
import os
from dotenv import load_dotenv
from textblob import TextBlob
import re

load_dotenv()

class RedditSentimentAnalyzer:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )