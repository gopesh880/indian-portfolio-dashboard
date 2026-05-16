
def calculate_health_score(df, risk_score):

    score = 100

    max_allocation = df["Allocation"].max()

    if max_allocation > 60:
        score -= 25

    if risk_score == "High":
        score -= 20

    if len(df) < 3:
        score -= 15

    return max(score, 0)

def generate_portfolio_insights(df, portfolio_return, risk_score):

    insights = []

    max_allocation = df["Allocation"].max()

    if max_allocation > 50:
        insights.append(
            "Your portfolio is heavily concentrated in one investment."
        )

    if risk_score == "High":
        insights.append(
            "Your portfolio may experience large short-term fluctuations."
        )

    if portfolio_return > 25:
        insights.append(
            "Your return expectations may be unrealistic long term."
        )

    crypto_exposure = df[df["Category"] == "Crypto"]["Allocation"].sum()

    if crypto_exposure > 20:
        insights.append(
            "Large crypto exposure increases volatility significantly."
        )

    if len(df) <= 2:
        insights.append(
            "Adding more asset classes may improve diversification."
        )

    return insights
