import pandas as pd
import plotly.express as px
from dash import dcc

def render_role_distribution_chart(df: pd.DataFrame):
    df["repo_count"] = pd.to_numeric(df["repo_count"], errors="coerce").fillna(0)
    top_langs = df.groupby("language")["repo_count"].sum().nlargest(20).index
    df_filtered = df[df["language"].isin(top_langs)]

    fig = px.bar(
        df_filtered,
        x="language",
        y="repo_count",
        color="language_role",
        barmode="stack",
        text="repo_count",        
    )
    fig.update_layout(
        dragmode=False,          
        xaxis_title=None,
        title=None
    )
    return dcc.Graph(id="role-distribution-chart", figure=fig)


def render_normalized_weight_chart(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="language",
        y="avg_percent_usage",
        text="avg_percent_usage", 
    )
    fig.update_layout(
        dragmode=False,
        xaxis_title=None,
        title=None
    )
    return dcc.Graph(id="normalized-weight-chart", figure=fig)