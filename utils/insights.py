# -------------------------------------------------
# HEALTH SCORE
# -------------------------------------------------

def calculate_health_score(
    df,
    risk_score
):

    score = 100

    # Highest allocation check
    max_allocation = df["Allocation (%)"].max()

    if max_allocation > 40:
        score -= 20

    # Number of investments
    if len(df) < 4:
        score -= 15

    # Risk adjustment
    if risk_score == "Very High":
        score -= 20

    elif risk_score == "High":
        score -= 10

    return max(score, 0)

# -------------------------------------------------
# PORTFOLIO INSIGHTS
# -------------------------------------------------

def generate_portfolio_insights(
    df,
    weighted_return,
    risk_score
):

    insights = []

    # Diversification insight
    if len(df) >= 6:

        insights.append(
            "Your portfolio appears well diversified across multiple asset categories."
        )

    else:

        insights.append(
            "Your portfolio may benefit from additional diversification."
        )

    # Return insight
    if weighted_return >= 15:

        insights.append(
            "Your expected return is relatively high, indicating strong growth potential but increased volatility."
        )

    elif weighted_return >= 10:

        insights.append(
            "Your portfolio has balanced long-term return expectations."
        )

    else:

        insights.append(
            "Your portfolio focuses more on stability and lower volatility."
        )

    # Risk insight
    if risk_score == "Very High":

        insights.append(
            "Your portfolio carries very high risk exposure and may experience large market fluctuations."
        )

    elif risk_score == "High":

        insights.append(
            "Your portfolio has moderate-to-high market risk exposure."
        )

    elif risk_score == "Moderate":

        insights.append(
            "Your portfolio maintains balanced risk exposure."
        )

    else:

        insights.append(
            "Your portfolio appears relatively conservative and stability-focused."
        )

    return insights
