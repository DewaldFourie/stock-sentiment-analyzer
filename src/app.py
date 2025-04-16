from flask import Flask, render_template, request, jsonify
from reddit_sentiment import RedditSentimentAnalyzer
from stock_data import StockDataFetcher
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize analyzers
sentiment_analyzer = RedditSentimentAnalyzer()
stock_fetcher = StockDataFetcher()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get stock symbol from form
        stock_symbol = request.form.get('stock_symbol', '').upper()
        
        # Get Reddit sentiment
        sentiment_data = sentiment_analyzer.analyze_sentiment(stock_symbol)
        
        # Get stock data
        stock_data = stock_fetcher.get_stock_data(stock_symbol)
        
        # Combine the data
        result = {
            'stock_symbol': stock_symbol,
            'sentiment': sentiment_data,
            'stock_data': stock_data
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True) 