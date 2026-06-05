
import yfinance as yf

def get_price_data(ticker):

    data = yf.download(
        ticker,
        start="2020-01-01",
        auto_adjust=True,
        progress=False
    )

    return data
