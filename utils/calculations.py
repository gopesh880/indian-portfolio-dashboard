import numpy as np


# ----------------------------------------
# WEIGHTED PORTFOLIO RETURN
# ----------------------------------------

def calculate_weighted_return(df):

    weights = df["Allocation (%)"] / 100

    returns = df["Expected Return (%)"]

    portfolio_return = np.sum(
        weights * returns
    )

    return round(portfolio_return, 2)


# ----------------------------------------
# PORTFOLIO RISK SCORE
# ----------------------------------------

def calculate_risk_score(df):

    risk_map = {
        "Low": 25,
        "Moderate": 50,
        "High": 75,
        "Very High": 100
    }

    weighted_risk = 0

    for _, row in df.iterrows():

        allocation = row["Allocation (%)"]

        risk = risk_map[row["Risk"]]

        weighted_risk += allocation * risk

    return round(weighted_risk / 100)


# ----------------------------------------
# RISK CATEGORY
# ----------------------------------------

def get_risk_category(risk_score):

    if risk_score <= 30:
        return "Low Risk"

    elif risk_score <= 60:
        return "Moderate Risk"

    elif risk_score <= 80:
        return "High Risk"

    else:
        return "Very High Risk"


# ----------------------------------------
# FUTURE VALUE (LUMP SUM)
# ----------------------------------------

def calculate_future_value(
    principal,
    annual_return,
    years
):

    rate = annual_return / 100

    future_value = principal * (
        (1 + rate) ** years
    )

    return round(future_value)


# ----------------------------------------
# FUTURE VALUE (SIP)
# ----------------------------------------

def calculate_sip_future_value(
    monthly_investment,
    annual_return,
    years
):

    monthly_rate = annual_return / 12 / 100

    months = years * 12

    future_value = monthly_investment * (
        (
            ((1 + monthly_rate) ** months) - 1
        ) / monthly_rate
    ) * (1 + monthly_rate)

    return round(future_value)


# ----------------------------------------
# INFLATION ADJUSTED VALUE
# ----------------------------------------

def calculate_inflation_adjusted_value(
    future_value,
    inflation_rate,
    years
):

    adjusted_value = future_value / (
        (1 + inflation_rate / 100) ** years
    )

    return round(adjusted_value)


# ----------------------------------------
# DIVERSIFICATION SCORE
# ----------------------------------------

def calculate_diversification_score(df):

    max_allocation = df["Allocation (%)"].max()

    if max_allocation <= 25:
        return 95

    elif max_allocation <= 40:
        return 80

    elif max_allocation <= 60:
        return 65

    else:
        return 40


# ----------------------------------------
# ALPHA
# ----------------------------------------

def calculate_alpha(
    portfolio_return,
    benchmark_return=12
):

    alpha = portfolio_return - benchmark_return

    return round(alpha, 2)


# ----------------------------------------
# SHARPE RATIO
# ----------------------------------------

def calculate_sharpe_ratio(
    portfolio_return,
    risk_score,
    risk_free_rate=7
):

    if risk_score == 0:
        return 0

    sharpe = (
        portfolio_return - risk_free_rate
    ) / (risk_score / 100)

    return round(sharpe, 2)


# ----------------------------------------
# PORTFOLIO SUMMARY
# ----------------------------------------

def calculate_portfolio_summary(df):

    weighted_return = calculate_weighted_return(df)

    risk_score = calculate_risk_score(df)

    diversification_score = calculate_diversification_score(df)

    alpha = calculate_alpha(weighted_return)

    sharpe_ratio = calculate_sharpe_ratio(
        weighted_return,
        risk_score
    )

    return {
        "weighted_return": weighted_return,
        "risk_score": risk_score,
        "diversification_score": diversification_score,
        "alpha": alpha,
        "sharpe_ratio": sharpe_ratio
    }
def calculate_sharpe_ratio(
    portfolio_return,
    risk_free_rate,
    volatility
):

    sharpe_ratio = (
        portfolio_return
        - risk_free_rate
    ) / volatility

    return round(
        sharpe_ratio,
        2
    )
