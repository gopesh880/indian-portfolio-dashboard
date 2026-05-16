
import plotly.express as px
import pandas as pd

def create_allocation_chart(df):

    fig = px.pie(
        df,
        values="Allocation",
        names="Asset",
        title="Portfolio Allocation"
    )

    fig.update_layout(template="plotly_dark")

    return fig

def create_returns_chart(df):

    fig = px.bar(
        df,
        x="Asset",
        y="Expected_Return",
        title="Expected Asset Returns"
    )

    fig.update_layout(template="plotly_dark")

    return fig

def create_growth_chart(initial_amount, annual_return, years):

    annual_return = annual_return / 100

    values = []
    timeline = []

    for year in range(years + 1):

        value = initial_amount * ((1 + annual_return) ** year)

        values.append(value)
        timeline.append(year)

    growth_df = pd.DataFrame({
        "Year": timeline,
        "Portfolio Value": values
    })

    fig = px.line(
        growth_df,
        x="Year",
        y="Portfolio Value",
        title="Portfolio Growth Projection"
    )

    fig.update_layout(template="plotly_dark")

    return fig

def create_monte_carlo_chart(simulation_df):

    fig = px.line(
        simulation_df,
        title="Monte Carlo Portfolio Simulation"
    )

    fig.update_layout(
        template="plotly_dark",
        showlegend=False
    )

    return fig
