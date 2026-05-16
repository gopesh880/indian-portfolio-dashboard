import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


TEMPLATE = "plotly_white"
COLORWAY = ["#2563EB", "#14B8A6", "#F59E0B", "#EF4444", "#8B5CF6", "#64748B"]


def _polish(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        colorway=COLORWAY,
        font={"family": "Inter, system-ui, sans-serif", "color": "#0F172A"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"l": 20, "r": 20, "t": 70, "b": 30},
        title={"font": {"size": 18, "color": "#0F172A"}},
        legend={"orientation": "h", "y": -0.18},
    )
    fig.update_xaxes(gridcolor="#E2E8F0", zerolinecolor="#CBD5E1")
    fig.update_yaxes(gridcolor="#E2E8F0", zerolinecolor="#CBD5E1")
    return fig


def create_allocation_chart(portfolio_df: pd.DataFrame) -> go.Figure:
    fig = px.pie(
        portfolio_df,
        names="Investment",
        values="Allocation (%)",
        title="Allocation by Investment",
        hole=0.45,
        template=TEMPLATE,
        color_discrete_sequence=COLORWAY,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return _polish(fig)


def create_returns_chart(portfolio_df: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        portfolio_df,
        x="Investment",
        y="Expected Return (%)",
        color="Risk",
        title="Expected Return by Investment",
        template=TEMPLATE,
        color_discrete_map={"Low": "#22C55E", "Medium": "#F59E0B", "High": "#EF4444"},
    )
    fig.update_layout(xaxis_title="", yaxis_title="Expected Return (%)")
    return _polish(fig)


def create_growth_chart(
    principal: float, annual_return: float, years: int
) -> go.Figure:
    timeline = list(range(years + 1))
    values = [principal * ((1 + annual_return / 100) ** year) for year in timeline]

    fig = go.Figure(
        data=[
            go.Scatter(
                x=timeline,
                y=values,
                mode="lines+markers",
                line={"color": "#2563EB", "width": 3},
                marker={"size": 7},
                name="Projected Value",
            )
        ]
    )
    fig.update_layout(
        title="Projected Portfolio Growth",
        xaxis_title="Year",
        yaxis_title="Portfolio Value",
        template=TEMPLATE,
    )
    return _polish(fig)


def create_monte_carlo_chart(simulation_df: pd.DataFrame) -> go.Figure:
    percentile_df = (
        simulation_df.groupby("Year")["Portfolio Value"]
        .quantile([0.1, 0.5, 0.9])
        .unstack()
        .reset_index()
        .rename(columns={0.1: "P10", 0.5: "Median", 0.9: "P90"})
    )

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=percentile_df["Year"],
            y=percentile_df["P90"],
            line={"width": 0},
            showlegend=False,
            name="P90",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=percentile_df["Year"],
            y=percentile_df["P10"],
            fill="tonexty",
            fillcolor="rgba(37, 99, 235, 0.18)",
            line={"width": 0},
            name="10th-90th percentile",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=percentile_df["Year"],
            y=percentile_df["Median"],
            mode="lines+markers",
            line={"color": "#F59E0B", "width": 3},
            name="Median outcome",
        )
    )
    fig.update_layout(
        title="Monte Carlo Outcome Range",
        xaxis_title="Year",
        yaxis_title="Portfolio Value",
        template=TEMPLATE,
    )
    return _polish(fig)