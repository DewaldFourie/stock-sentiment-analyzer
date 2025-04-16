
# 📈 Reddit Stock Sentiment Analyze

Track the hype before the spike. This tool scrapes Reddit for real-time stock discussions, analyzes sentiment using NLP, and blends it with live market data — giving you a street-level view of what the retail crowd is thinking.


## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Create a .env file with your Reddit API credentials:

```bash
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
```
3. Run the main Script: 
```bash
python stock_sentiment.py
```
OR
```bash
python src/app.py
```
## Features

- 📊 Real-Time Sentiment Analysis
- 🧵 Reddit Post Parsing
- 📈 Stock Data Integration
- 🧠 Sentiment Analysis via NLPs
- 📉 Correlates Sentiment with Market Data
- 📊 Trend Prediction



## Tech Stack

- **Backend Framework:** Flask (Python)  
- **Sentiment Analysis:** TextBlob  
- **Reddit API:** PRAW (Python Reddit API Wrapper)  
- **Stock Market Data:** Yahoo Finance API  
- **Frontend:** HTML with Jinja2 templating  
- **Environment Management:** python-dotenv, pyenv  
- **Data Format:** JSON  
- **Hosting:** Local Flask development servers




## Authors

- [@dewaldfourie](https://github.com/DewaldFourie)


## License

[MIT](https://choosealicense.com/licenses/mit/)


## Support

For support, email dewaldfourie0808@gmail.com or visit https://portfolio-website-pied-five.vercel.app/

