import praw
import pandas as pd
import numpy as np
import yfinance as yf
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import nltk

# Download required NLTK data
nltk.download('vader_lexicon')

# Load environment variables
load_dotenv()


