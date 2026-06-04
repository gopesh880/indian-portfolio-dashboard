import pandas as pd

def get_investment_suggestions(profile):

    suggestions = {

        "Conservative": [

            {
                "Investment": "HDFC Corporate Bond Fund",
                "Category": "Debt Fund",
                "Risk": "Low",
                "Why": "Suitable for investors looking for relatively stable long-term returns."
            },

            {
                "Investment": "ICICI Prudential Equity & Debt Fund",
                "Category": "Hybrid Fund",
                "Risk": "Moderate",
                "Why": "Balanced exposure to both equity and debt investments."
            },

            {
                "Investment": "Power Grid Corporation",
                "Category": "Dividend Stock",
                "Risk": "Moderate",
                "Why": "Historically stable company with consistent dividend payouts."
            },

            {
                "Investment": "Coal India",
                "Category": "Dividend Stock",
                "Risk": "Moderate",
                "Why": "Known for strong dividends and relatively stable cash flows."
            },

            {
                "Investment": "SBI Magnum Gilt Fund",
                "Category": "Government Debt Fund",
                "Risk": "Low",
                "Why": "Provides exposure to government-backed securities."
            },

            {
                "Investment": "HDFC Balanced Advantage Fund",
                "Category": "Balanced Fund",
                "Risk": "Moderate",
                "Why": "Dynamically balances equity and debt exposure."
            }

        ],

        "Moderate": [

            {
                "Investment": "Parag Parikh Flexi Cap Fund",
                "Category": "Flexi Cap Fund",
                "Risk": "Moderate",
                "Why": "Diversified exposure across Indian and international companies."
            },

            {
                "Investment": "Trent",
                "Category": "Consumer Growth Stock",
                "Risk": "High",
                "Why": "Strong long-term growth in Indian retail and consumer spending."
            },

            {
                "Investment": "Polycab India",
                "Category": "Manufacturing Stock",
                "Risk": "High",
                "Why": "Beneficiary of India's infrastructure and manufacturing expansion."
            },

            {
                "Investment": "Titan",
                "Category": "Consumer Stock",
                "Risk": "Moderate",
                "Why": "Strong brand value and consistent long-term growth."
            },

            {
                "Investment": "Motilal Oswal Midcap Fund",
                "Category": "Mid Cap Fund",
                "Risk": "High",
                "Why": "Provides exposure to fast-growing mid-sized companies."
            },

            {
                "Investment": "Avenue Supermarts",
                "Category": "Retail Growth Stock",
                "Risk": "High",
                "Why": "Long-term growth linked to rising Indian consumption."
            }

        ],

        "Aggressive": [

            {
                "Investment": "KPIT Technologies",
                "Category": "AI & EV Technology",
                "Risk": "Very High",
                "Why": "Focused on automotive software and electric vehicle technologies."
            },

            {
                "Investment": "Tata Elxsi",
                "Category": "Technology Growth Stock",
                "Risk": "High",
                "Why": "Strong presence in design, AI, and engineering technology services."
            },

            {
                "Investment": "Nippon India Small Cap Fund",
                "Category": "Small Cap Fund",
                "Risk": "Very High",
                "Why": "Provides exposure to emerging small-cap growth companies."
            },

            {
                "Investment": "Deepak Nitrite",
                "Category": "Chemical Growth Stock",
                "Risk": "High",
                "Why": "Strong growth potential in specialty chemicals sector."
            },

            {
                "Investment": "HAL",
                "Category": "Defense Stock",
                "Risk": "High",
                "Why": "Potential beneficiary of India's defense manufacturing growth."
            },

            {
                "Investment": "Quant Small Cap Fund",
                "Category": "High Growth Fund",
                "Risk": "Very High",
                "Why": "Aggressive small-cap focused investment strategy."
            }

        ]
    }

    return pd.DataFrame(suggestions[profile])
def get_asset_allocation(profile):

```
allocations = {

    "Conservative": {
        "Equity": 40,
        "Debt": 50,
        "Gold": 10,
        "Expected Return": 8,
        "Risk Score": "Low"
    },

    "Moderate": {
        "Equity": 60,
        "Debt": 30,
        "Gold": 10,
        "Expected Return": 11,
        "Risk Score": "Moderate"
    },

    "Aggressive": {
        "Equity": 80,
        "Debt": 10,
        "Gold": 10,
        "Expected Return": 14,
        "Risk Score": "High"
    }

}

return allocations[profile]
```
