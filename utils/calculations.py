import numpy as np

# -------------------------------------------------
# WEIGHTED RETURN
# -------------------------------------------------

def calculate_weighted_return(df):

    weights = df["Allocation (%)"] / 100

    returns = df["Expected Return (%)"]

    portfolio_return = np.sum(
        weights * returns
    )

    return round(portfolio_return, 2)

# -------------------------------------------------
# RISK SCORE
# -------------------------------------------------

def calculate_risk_score(df):

    risk_map = {
        "Low": 1,
        "Moderate": 2,
        "High": 3,
        "Very High": 4
    }

    weighted_risk = 0

    for _, row in df.iterrows():

        allocation = row["Allocation (%)"]

        risk = risk_map[row["Risk"]]

        weighted_risk += allocation * risk

    average_risk = weighted_risk / 100

    if average_risk <= 1.5:
        return "Low"

    elif average_risk <= 2.5:
        return "Moderate"

    elif average_risk <= 3.5:
        return "High"

    else:
        return "Very High"

# -------------------------------------------------
# FUTURE VALUE
# -------------------------------------------------

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

# -------------------------------------------------
# SIP FUTURE VALUE
# -------------------------------------------------

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

# -------------------------------------------------
# INFLATION ADJUSTED VALUE
# -------------------------------------------------

def calculate_inflation_adjusted_value(
    future_value,
    inflation_rate,
    years
):

    adjusted_value = future_value / (
        (1 + inflation_rate / 100) ** years
    )

    return round(adjusted_value)

# -------------------------------------------------
# DIVERSIFICATION SCORE
# -------------------------------------------------

def calculate_diversification_score(df):

    number_of_assets = len(df)

    if number_of_assets >= 6:
        return 90

    elif number_of_assets >= 4:
        return 75

    else:
        return 50
