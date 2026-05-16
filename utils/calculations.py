
import numpy as np

def calculate_weighted_return(df):
    weights = df["Allocation"] / 100
    returns = df["Expected_Return"]
    return np.sum(weights * returns)

def calculate_risk_score(df):
    crypto = df[df["Category"] == "Crypto"]["Allocation"].sum()
    equity = df[df["Category"] == "Equity"]["Allocation"].sum()

    risk_value = crypto * 1.5 + equity

    if risk_value < 30:
        return "Low"
    elif risk_value < 60:
        return "Moderate"
    else:
        return "High"

def calculate_future_value(principal, annual_return, years):
    annual_return = annual_return / 100
    return principal * ((1 + annual_return) ** years)

def calculate_sip_future_value(monthly_sip, annual_return, years):
    monthly_rate = annual_return / 12 / 100
    months = years * 12

    future_value = (
        monthly_sip
        * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        * (1 + monthly_rate)
    )

    return future_value

def calculate_inflation_adjusted_value(value, inflation_rate, years):
    inflation_rate = inflation_rate / 100
    return value / ((1 + inflation_rate) ** years)

def calculate_diversification_score(df):
    unique_assets = len(df)

    if unique_assets >= 5:
        return 90
    elif unique_assets >= 3:
        return 70
    else:
        return 40
