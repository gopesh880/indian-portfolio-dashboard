import plotly.express as px
import pandas as pd

# -------------------------------------------------
# PORTFOLIO ALLOCATION PIE CHART
# -------------------------------------------------

def create_allocation_chart(df):

    fig = px.pie(
        df,
        names="Investment",
        values="Allocation (%)",
        title="Portfolio Allocation"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig

# -------------------------------------------------
# RETURNS BAR CHART
# -------------------------------------------------

def create_returns_chart(df):

    fig = px.bar(
        df,
        x="Investment",
        y="Expected Return (%)",
        color="Expected Return (%)",
        title="Expected Asset Returns"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig

# -------------------------------------------------
# INVESTMENT GROWTH CHART
# -------------------------------------------------

def create_growth_chart(
    principal,
    annual_return,
    years
):

    growth_data = []

    current_value = principal

    for year in range(years + 1):

        growth_data.append({
            "Year": year,
            "Portfolio Value": round(current_value)
        })

        current_value *= (
            1 + annual_return / 100
        )

    growth_df = pd.DataFrame(
        growth_data
    )

    fig = px.line(
        growth_df,
        x="Year",
        y="Portfolio Value",
        title="Projected Portfolio Growth"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig

# -------------------------------------------------
# MONTE CARLO CHART
# -------------------------------------------------

def create_monte_carlo_chart(simulation_df):

    fig = px.line(
        simulation_df,
        title="Monte Carlo Portfolio Simulation"
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Years",
        yaxis_title="Portfolio Value"
    )

    return fig
