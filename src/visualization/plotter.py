import matplotlib
matplotlib.use('Agg')  # Set the backend to non-interactive
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import os


class SentimentPlotter:
    def __init__(self):
        plt.style.use('seaborn')
        self.figsize = (12, 8)

    def plot_sentiment_trend(self, sentiment_data, stock_data=None, title="Sentiment Analysis"):
        """Plot sentiment trend with optional stock price overlay"""
        if sentiment_data.empty:
            # Create an empty plot if no data
            fig, ax = plt.subplots(figsize=self.figsize)
            ax.text(0.5, 0.5, 'No sentiment data available', 
                horizontalalignment='center', verticalalignment='center')
            plt.title(title)
            return fig
            
        fig, ax1 = plt.subplots(figsize=self.figsize)
        
        # Plot sentiment
        color = 'tab:blue'
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Sentiment Score', color=color)
        ax1.plot(sentiment_data.index, sentiment_data.values, color=color, label='Sentiment')
        ax1.tick_params(axis='y', labelcolor=color)
        
        # Add stock price if provided
        if stock_data is not None and not stock_data.empty:
            ax2 = ax1.twinx()
            color = 'tab:red'
            ax2.set_ylabel('Stock Price', color=color)
            ax2.plot(stock_data.index, stock_data['Close'], color=color, label='Stock Price')
            ax2.tick_params(axis='y', labelcolor=color)
        
        plt.title(title)
        fig.tight_layout()
        return fig
    
    def plot_sentiment_distribution(self, sentiment_scores, title="Sentiment Distribution"):
        """Plot distribution of sentiment scores"""
        plt.figure(figsize=self.figsize)
        if len(sentiment_scores) > 0:
            sns.histplot(sentiment_scores, kde=True)
        else:
            plt.text(0.5, 0.5, 'No sentiment data available',
                    horizontalalignment='center', verticalalignment='center')
        plt.title(title)
        plt.xlabel('Sentiment Score')
        plt.ylabel('Frequency')
        return plt.gcf()
    
    def plot_quality_scores(self, posts_df, title="Post Quality Distribution"):
        """Plot distribution of post quality scores"""
        plt.figure(figsize=self.figsize)
        if 'quality_score' in posts_df.columns and len(posts_df) > 0:
            sns.histplot(posts_df['quality_score'], kde=True)
        else:
            plt.text(0.5, 0.5, 'No quality score data available',
                    horizontalalignment='center', verticalalignment='center')
        plt.title(title)
        plt.xlabel('Quality Score')
        plt.ylabel('Frequency')
        return plt.gcf()
    
    def plot_sentiment_vs_price(self, sentiment_data, stock_data, title="Sentiment vs Stock Price"):
        """Plot sentiment scores against stock price"""
        plt.figure(figsize=self.figsize)
        
        if len(sentiment_data) > 0 and not stock_data.empty:
            plt.scatter(sentiment_data, stock_data['Close'])
            
            # Add trend line
            try:
                z = np.polyfit(sentiment_data, stock_data['Close'], 1)
                p = np.poly1d(z)
                plt.plot(sentiment_data, p(sentiment_data), "r--")
            except Exception as e:
                print(f"Error creating trend line: {str(e)}")
        else:
            plt.text(0.5, 0.5, 'Insufficient data for correlation plot',
                    horizontalalignment='center', verticalalignment='center')
            
        plt.title(title)
        plt.xlabel('Sentiment Score')
        plt.ylabel('Stock Price')
        return plt.gcf()
    
    def save_plot(self, fig, filename):
        """Save plot to file"""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            fig.savefig(filename)
        except Exception as e:
            print(f"Error saving plot: {str(e)}")
        finally:
            plt.close(fig) 