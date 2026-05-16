
import streamlit as st
import pandas as pd
from utils.recommendations import get_investment_suggestions

from utils.calculations import (
    calculate_weighted_return,
    calculate_risk_score,
    calculate_future_value,
    calculate_sip_future_value,
    calculate_inflation_adjusted_value,
    calculate_diversification_score
)

from utils.insights import (
    generate_portfolio_insights,
    calculate_health_score
)

from utils.simulations import monte_carlo_simulation

from charts.portfolio_charts import (
    create_allocation_chart,
    create_returns_chart,
    create_growth_chart,
    create_monte_carlo_chart
)

st.set_page_config(
    page_title="Indian Portfolio Dashboard",
    layout="wide"
)

st.title("Indian Portfolio & Risk Intelligence Dashboard")

st.markdown(
    '''
    A practical finance analytics platform for Indian retail investors.
    '''
)

st.sidebar.header("Investor Inputs")

investment_amount = st.sidebar.number_input(
    "Investment Amount (₹)",
    min_value=1000,
    value=500000
)

sip_amount = st.sidebar.number_input(
    "Monthly SIP Amount (₹)",
    min_value=0,
    value=10000
)

investment_duration = st.sidebar.slider(
    "Investment Duration (Years)",
    1,
    40,
    15
)

investor_profile = st.sidebar.selectbox(
    "Investor Profile",
    ["Conservative", "Moderate", "Aggressive"]
)

portfolio_df = pd.read_csv("data/sample_portfolio.csv")

weighted_return = calculate_weighted_return(portfolio_df)

risk_score = calculate_risk_score(portfolio_df)

future_value = calculate_future_value(
    investment_amount,
    weighted_return,
    investment_duration
)

sip_future_value = calculate_sip_future_value(
    sip_amount,
    weighted_return,
    investment_duration
)

inflation_adjusted_value = calculate_inflation_adjusted_value(
    future_value,
    6,
    investment_duration
)

diversification_score = calculate_diversification_score(
    portfolio_df
)

health_score = calculate_health_score(
    portfolio_df,
    risk_score
)

simulation_df = monte_carlo_simulation(
    investment_amount,
    weighted_return,
    18,
    investment_duration
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Expected Return",
    f"{weighted_return:.2f}%"
)

col2.metric(
    "Risk Score",
    risk_score
)

col3.metric(
    "Portfolio Health",
    f"{health_score}/100"
)

col4.metric(
    "Diversification",
    f"{diversification_score}/100"
)

st.divider()

col5, col6 = st.columns(2)

col5.metric(
    "Projected Portfolio Value",
    f"₹{future_value:,.0f}"
)

col6.metric(
    "Inflation Adjusted Value",
    f"₹{inflation_adjusted_value:,.0f}"
)

st.metric(
    "Projected SIP Value",
    f"₹{sip_future_value:,.0f}"
)

allocation_chart = create_allocation_chart(portfolio_df)
returns_chart = create_returns_chart(portfolio_df)
growth_chart = create_growth_chart(
    investment_amount,
    weighted_return,
    investment_duration
)

monte_carlo_chart = create_monte_carlo_chart(
    simulation_df
)

chart_col1, chart_col2 = st.columns(2)

chart_col1.plotly_chart(allocation_chart, use_container_width=True)
chart_col2.plotly_chart(returns_chart, use_container_width=True)

st.plotly_chart(growth_chart, use_container_width=True)

st.plotly_chart(monte_carlo_chart, use_container_width=True)

st.subheader("Portfolio Breakdown")

st.dataframe(portfolio_df)

st.subheader("Investor Insights")

insights = generate_portfolio_insights(
    portfolio_df,
    weighted_return,
    risk_score
)

for insight in insights:
    st.warning(insight)

st.subheader("Beginner Finance Education")

st.info(
    "Diversification means spreading investments across different assets to reduce overall risk."
)

st.info(
    "SIP investing helps investors build wealth consistently over long periods."
)

st.info(
    "Inflation reduces purchasing power over time, which is why inflation-adjusted returns matter."
)
st.info(
    "Inflation reduces purchasing power over time, which is why inflation-adjusted returns matter."
)


st.subheader("Suggested Investments For Your Profile")

recommendation_df = get_investment_suggestions(
    investor_profile
)

st.dataframe(recommendation_df)

for _, row in recommendation_df.iterrows():

    st.success(
        f"{row['Investment']} ({row['Category']})\n\n"
        f"Risk Level: {row['Risk']}\n\n"
        f"Why Suggested: {row['Why']}"
    )
