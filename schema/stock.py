import yfinance as yf
from datetime import datetime, timedelta

def fetch_stock_data(ticker: str):
    one_year_ago = datetime.now() - timedelta(days=365)
    stock = yf.Ticker(ticker)
    current_price = stock.info.get("currentPrice") or stock.info.get("bid")
    dividends = stock.dividends[stock.dividends.index >= one_year_ago.strftime("%Y-%m-%d")]

    return {
        "ticker": ticker,
        "market_price": current_price,
        "dividends": dividends.to_dict()
    }

def resolve_stock(*_, ticker: str):
    stock_data = fetch_stock_data(ticker)
    if not stock_data:
        return None
    return {
        "ticker": stock_data["ticker"],
        "marketPrice": stock_data["market_price"],
        "dividends": [{"date": date.strftime("%Y-%m-%d"), "value": value} for date, value in stock_data["dividends"].items()]
    }
