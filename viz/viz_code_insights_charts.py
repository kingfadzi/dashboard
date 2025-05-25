import plotly.express as px
import pandas as pd
from dash import dcc

def render_role_distribution_chart(df: pd.DataFrame):
    top_langs = df.groupby("Language")["Repo Count"].sum().nlargest(20).index
    df_filtered = df[df["Language"].isin(top_langs)]
    fig = px.bar(
        df_filtered,
        x="Language",
        y="Repo Count",
        color="Role",
        barmode="stack",
        title="Language Role Distribution (Top 20)",
    )
    return dcc.Graph(id="role-distribution-chart", figure=fig)

def render_normalized_weight_chart(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="Language",
        y="Avg Percent Usage",
        title="Normalized Language Weight (Top 20)",
    )
    return dcc.Graph(id="normalized-weight-chart", figure=fig)
