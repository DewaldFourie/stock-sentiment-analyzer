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

    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove Reddit-style links
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        # Remove special characters and digits
        text = re.sub(r'[^\w\s]', '', text)
        return text.strip()
    
    def get_sentiment_score(self, text):
        cleaned_text = self.clean_text(text)
        if not cleaned_text:
            return 0
        
        analysis = TextBlob(cleaned_text)
        return analysis.sentiment.polarity
    
    def get_reddit_posts(self, stock_symbol, limit=100):
        posts = []
        try:
            for post in self.reddit.subreddit('stocks+investing+wallstreetbets').search(
                f'{stock_symbol} stock', limit=limit, time_filter='month'
            ):
            
                full_text = f"{post.title} {post.selftext}"
                sentiment_score = self.get_sentiment_score(full_text)
                
                posts.append({
                    'title': post.title,
                    'text': post.selftext,
                    'score': post.score,
                    'sentiment': sentiment_score,
                    'created_utc': datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                    'url': f'https://reddit.com{post.permalink}',
                    'subreddit': post.subreddit.display_name
                })
        except Exception as e:
            print(f"Error fetching Reddit posts: {str(e)}")
        return pd.DataFrame(posts)

    def analyze_sentiment(self, stock_symbol):
            posts_df = self.get_reddit_posts(stock_symbol)
            
            if len(posts_df) == 0:
                return {
                    'success': False,
                    'error': f'No Reddit posts found for {stock_symbol}'
                }
            
            avg_sentiment = posts_df['sentiment'].mean()
            

            posts_df['sentiment_category'] = posts_df['sentiment'].apply(
                lambda x: 'positive' if x > 0 else ('negative' if x < 0 else 'neutral')
            )
            
            sentiment_counts = posts_df['sentiment_category'].value_counts().to_dict()
            

            top_posts = posts_df.nlargest(5, 'score').to_dict('records')
            
            return {
                'success': True,
                'average_sentiment': float(avg_sentiment),
                'post_count': len(posts_df),
                'sentiment_distribution': sentiment_counts,
                'top_posts': top_posts
            } 