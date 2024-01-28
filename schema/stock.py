import yfinance as yf
from datetime import datetime, timedelta
from typing import List

def fetch_stock_data(tickers: List[str]):
    stock_data = []
    one_year_ago = datetime.now() - timedelta(days=365)
    
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        current_price = stock.info.get("currentPrice") or stock.info.get("bid")
        dividends = stock.dividends[stock.dividends.index >= one_year_ago.strftime("%Y-%m-%d")]

        stock_data.append({
            "ticker": ticker,
            "market_price": current_price,
            "dividends": dividends.to_dict()
        })

    return stock_data


def resolve_stocks(*_, tickers: List[str]):
    data = fetch_stock_data(tickers)
    return [
        {
            "ticker": stock["ticker"],
            "marketPrice": stock["market_price"],
            "dividends": [{"date": date.strftime("%Y-%m-%d"), "value": value} for date, value in stock["dividends"].items()]
        }
        for stock in data
    ]

