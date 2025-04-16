import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import nltk

class EnhancedSentimentAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.classifier = RandomForestClassifier(n_estimators=100)
        self.stop_words = set(stopwords.words('english'))
        self.quality_threshold = 0.5  

    def preprocess_text(self, text):
        """Preprocess text for analysis"""
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in self.stop_words]
        return ' '.join(tokens)
    
    def calculate_quality_score(self, post):
        """Calculate quality score for a post"""
        score = 0

        if len(post['text']) > 100:
            score += 0.3

        if post['score'] > 10:
            score += 0.3

        sentiment_scores = self.sia.polarity_scores(post['text'])
        score += abs(sentiment_scores['compound']) * 0.4
        return score
    
    def filter_low_quality_posts(self, posts_df):
        """Filter out low quality posts"""
        posts_df['quality_score'] = posts_df.apply(self.calculate_quality_score, axis=1)
        return posts_df[posts_df['quality_score'] > self.quality_threshold]
    
    def analyze_sentiment(self, text):
        """Enhanced sentiment analysis using both VADER and custom features"""

        vader_sentiment = self.sia.polarity_scores(text)
        
    
        text_length = len(text)
        word_count = len(text.split())
        has_question = 1 if '?' in text else 0
        has_exclamation = 1 if '!' in text else 0
        
    
        sentiment_score = (
            vader_sentiment['compound'] * 0.7 +  
            (text_length / 1000) * 0.1 +  
            (has_question * -0.1) +  
            (has_exclamation * 0.1)  
        )
        
        return sentiment_score
    
    def analyze_trend(self, posts_df, window_size=7):
        """Analyze sentiment trend over time"""
        if len(posts_df) == 0:
            return {
                'trend': 'Neutral',
                'daily_sentiment': pd.Series(),
                'moving_avg': pd.Series(),
                'current_sentiment': 0
            }
            
        posts_df['date'] = pd.to_datetime(posts_df['created_utc'])
        posts_df.set_index('date', inplace=True)
        

        daily_sentiment = posts_df['sentiment'].resample('D').mean()
        
        moving_avg = daily_sentiment.rolling(window=window_size).mean()
        
    
        trend = 'Neutral'
        if len(moving_avg) > 0:
            if moving_avg.iloc[-1] > 0.2:
                trend = 'Bullish'
            elif moving_avg.iloc[-1] < -0.2:
                trend = 'Bearish'
        
        return {
            'trend': trend,
            'daily_sentiment': daily_sentiment,
            'moving_avg': moving_avg,
            'current_sentiment': moving_avg.iloc[-1] if len(moving_avg) > 0 else 0
        } 