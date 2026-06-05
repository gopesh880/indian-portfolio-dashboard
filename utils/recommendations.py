import pandas as pd
def get_investment_suggestions(profile, goal):

    suggestions = {

        ("Conservative", "Retirement"): [
            {
                "Investment": "HDFC Balanced Advantage Fund",
                "Category": "Hybrid Fund",
                "Risk": "Moderate",
                "Why": "Suitable for long-term retirement planning with balanced risk."
            },
            {
                "Investment": "HDFC Corporate Bond Fund",
                "Category": "Debt Fund",
                "Risk": "Low",
                "Why": "Provides stability and predictable income."
            },
        ],

        ("Moderate", "Wealth Creation"): [
            {
                "Investment": "HDFC Flexi Cap Fund",
                "Category": "Flexi Cap Fund",
                "Risk": "Moderate",
                "Why": "Diversified exposure across sectors and market caps."
            },
            {
                "Investment": "HDFC Mid-Cap Opportunities Fund",
                "Category": "Mid Cap Fund",
                "Risk": "High",
                "Why": "Potential for higher long-term growth."
            },
        ],

        ("Aggressive", "Wealth Creation"): [
            {
                "Investment": "HDFC Flexi Cap Fund",
                "Category": "Flexi Cap Fund",
                "Risk": "Moderate",
                "Why": "Core equity allocation."
            },
            {
                "Investment": "HDFC Mid-Cap Opportunities Fund",
                "Category": "Mid Cap Fund",
                "Risk": "High",
                "Why": "Higher growth potential."
            },
            {
                "Investment": "HDFC Small Cap Fund",
                "Category": "Small Cap Fund",
                "Risk": "Very High",
                "Why": "Aggressive long-term wealth creation."
            },
        ],
    }

    return pd.DataFrame(
        suggestions.get(
            (profile, goal),
            suggestions[("Moderate", "Wealth Creation")]
        )
    )
def get_asset_allocation(profile):

    allocations = {
        "Conservative": {
            "Equity": 40,
            "Debt": 50,
            "Gold": 10,
        },
        "Moderate": {
            "Equity": 60,
            "Debt": 30,
            "Gold": 10,
        },
        "Aggressive": {
            "Equity": 80,
            "Debt": 10,
            "Gold": 10,
        },
    }

    return allocations[profile]
def get_rebalancing_suggestions(
    current_allocation,
    target_allocation
):

    suggestions = []

    for asset in current_allocation:

        difference = (
            target_allocation[asset]
            - current_allocation[asset]
        )

        if difference > 0:

            suggestions.append(
                f"Buy {difference}% {asset}"
            )

        elif difference < 0:

            suggestions.append(
                f"Sell {abs(difference)}% {asset}"
            )

        else:

            suggestions.append(
                f"No change in {asset}"
            )

    return suggestions
