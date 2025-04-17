from flask import Flask, render_template, request, jsonify
from reddit_sentiment import RedditSentimentAnalyzer
from stock_data import StockDataFetcher
from visualization.plotter import SentimentPlotter
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize analyzers
sentiment_analyzer = RedditSentimentAnalyzer()
stock_fetcher = StockDataFetcher()
plotter = SentimentPlotter()

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

        # Convert to DataFrames if needed
        sentiment_df = sentiment_data.get('dataframe')  # assuming you return this from analyzer
        stock_df = stock_data.get('dataframe')  # assuming you return this from fetcher

        # Generate and save plots
        plot_paths = []

        if sentiment_df is not None:
            fig1 = plotter.plot_sentiment_trend(sentiment_df, stock_df)
            path1 = f'static/plots/{stock_symbol}_trend.png'
            plotter.save_plot(fig1, path1)
            plot_paths.append(path1)

            fig2 = plotter.plot_sentiment_distribution(sentiment_df.values)
            path2 = f'static/plots/{stock_symbol}_dist.png'
            plotter.save_plot(fig2, path2)
            plot_paths.append(path2)

            if stock_df is not None:
                fig3 = plotter.plot_sentiment_vs_price(sentiment_df.values, stock_df)
                path3 = f'static/plots/{stock_symbol}_correlation.png'
                plotter.save_plot(fig3, path3)
                plot_paths.append(path3)
        
        # Combine the data
        result = {
            'stock_symbol': stock_symbol,
            'sentiment': sentiment_data,
            'stock_data': stock_data,
            'plot_paths': plot_paths
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True) 