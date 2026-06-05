import yfinance as yf

def get_price_data(ticker):

    data = yf.download(
        ticker,
        period="5y",
        auto_adjust=True
    )

    return data
