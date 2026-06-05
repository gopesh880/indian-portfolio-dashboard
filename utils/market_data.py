import yfinance as yf


def get_price_data(ticker):

    data = yf.download(
        ticker,
        period="5y",
        progress=False,
        auto_adjust=True
    )

    return data
