import yfinance as yf
import time
from requests.exceptions import HTTPError

class StockDataFetcher:
    def get_stock_data(self, stock_symbol, max_retries=3, retry_delay=5):
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    time.sleep(retry_delay)
                
                stock = yf.Ticker(stock_symbol)
                
                try:
                    current_price = stock.info.get('currentPrice')
                    if current_price is None:
                        raise ValueError(f"Could not get current price for {stock_symbol}")
                        
                    return {
                        'success': True,
                        'data': {
                            'current_price': current_price,
                            'currency': stock.info.get('currency', 'USD')
                        }
                    }
                    
                except HTTPError as e:
                    if e.response.status_code == 429:
                        print(f"Rate limit hit, attempt {attempt + 1} of {max_retries}")
                        if attempt == max_retries - 1:
                            raise ValueError("Rate limit exceeded. Please try again later.")
                        continue
                    raise
                
            except Exception as e:
                print(f"Error fetching stock data (attempt {attempt + 1}): {str(e)}")
                if attempt == max_retries - 1:
                    return {
                        'success': False,
                        'error': f"Failed to fetch stock data for {stock_symbol} after {max_retries} attempts: {str(e)}"
                    }
                continue 