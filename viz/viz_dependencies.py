from components.chart_style import standard_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


@standard_chart_style
def render_dependency_detection_chart(df):
    return px.bar(
        df,
        x="status",
        y="repo_count",
        color="status",
        text="repo_count",
        labels={"status": "", "repo_count": "Repository Count"},
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )

@standard_chart_style
def render_iac_detection_chart(df):
    return px.bar(
        df,
        x="status",
        y="repo_count",
        text="repo_count",
        color="status",
        labels={"status": "", "repo_count": "Repository Count"},
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )

@standard_chart_style
def render_xeol_detection_chart(df):
    return px.bar(
        df,
        x="status",
        y="repo_count",
        color="status",
        text="repo_count",
        labels={"status": "", "repo_count": "Repository Count"},
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )


@standard_chart_style
def render_package_type_distribution_chart(df):
    fig = px.bar(
        df,
        y="package_type",
        x="repo_count",
        color="package_type",
        orientation="h",
        text="repo_count",
        labels={"package_type": "", "repo_count": "Repository Count"},
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )

    fig.update_layout(
        showlegend=False,
        xaxis=dict(
            showticklabels=True,
            title="Repository Count"
        )
    )

    return fig


@standard_chart_style
def render_subcategory_distribution_chart(df):
    fig = px.bar(
        df,
        x="sub_category",
        y="repo_count",
        text="repo_count",
        color="package_type",
        labels={
            "sub_category": "",
            "repo_count": "Repository Count",
            "package_type": "Package Type"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )
    fig.update_xaxes(showticklabels=True)
    return fig

@standard_chart_style
def render_dependency_volume_chart(df):
    fig = px.bar(
        df,
        x="dep_bucket",
        y="repo_count",
        color="main_language",
        text="repo_count",
        labels={"dep_bucket": "Dependency Count", "repo_count": "Repository Count"},
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )
    fig.update_layout(
        xaxis_title="Dependency Count",
        legend=dict(
            orientation="h",
            y=1.02,
            x=0.5,
            xanchor="center",
            font=dict(size=10)
        )
    )
    fig.update_layout(
        barmode="stack",
        xaxis=dict(type="category", showticklabels=True)
    )
    return fig


@standard_chart_style
def render_xeol_top_products_chart(df):
    fig = px.bar(
        df,
        x="eol_state",
        y="repo_count",
        color="artifact_type",
        text="repo_count",
        labels={
            "eol_state": "EOL Status",
            "repo_count": "Repository Count",
            "artifact_type": "Artifact Type"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )

    fig.update_layout(
        barmode="stack",
        xaxis=dict(type="category", showticklabels=True)
    )

    return fig

from plotly.graph_objects import Figure, Bar

@standard_chart_style
def render_iac_category_summary_chart(df):
    if df is None or df.empty:
        return px.bar(title="No IaC category data available")

    fig = Figure()

    # Bar: Repository Count (left axis)
    fig.add_trace(
        Bar(
            y=df["category"],
            x=df["repo_count"],
            name="Repository Count",
            orientation="h",
            xaxis="x1",
            offsetgroup=0,
            text=df["repo_count"],
            textposition="outside",
            marker_color="#1f77b4"
        )
    )

    # Bar: Framework Count (right axis)
    fig.add_trace(
        Bar(
            y=df["category"],
            x=df["framework_count"],
            name="Framework Count",
            orientation="h",
            xaxis="x2",
            offsetgroup=1,
            text=df["framework_count"],
            textposition="outside",
            marker_color="#9467bd"
        )
    )

    fig.update_layout(
        title="IaC Categories: Repository Count vs Framework Diversity",
        barmode="group",
        yaxis=dict(title="Category", automargin=True),

        # Left x-axis
        xaxis=dict(
            title="Repository Count",
            side="bottom",
            showgrid=True,
            zeroline=True
        ),

        # Right x-axis
        xaxis2=dict(
            title="Framework Count",
            overlaying="x",
            side="top",
            showgrid=False,
            zeroline=True
        ),

        legend=dict(
            orientation="h",
            y=1.05,
            x=0.5,
            xanchor="center",
            font=dict(size=10)
        )
    )

    return fig


@standard_chart_style
def render_iac_adoption_by_framework_count_chart(df):
    # Ensure the buckets appear in the desired order:
    category_order = ["0 (none)", "1", "2–4", "5–7", "8+"]

    fig = px.bar(
        df,
        x="framework_bucket",
        y="repo_count",
        color="classification_label",
        barmode="stack",
        text="repo_count",
        category_orders={"framework_bucket": category_order},
        labels={
            "framework_bucket": "Frameworks Used per Repository",
            "repo_count": "Repository Count",
            "classification_label": "Classification"
        }
    )

    fig.update_traces(
        texttemplate="%{text}",
        textposition="inside",
        textfont_size=12
    )

    fig.update_layout(
        title=None,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Frameworks Used per Repository",
        yaxis_title="Repository Count"
    )

    fig.update_xaxes(showticklabels=True)

    return fig





from components.chart_style import standard_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE
import plotly.express as px

@standard_chart_style
def render_top_expired_xeol_products_chart(df):
    df["product_label"] = df["artifact_name"].apply(
        lambda x: x if len(x) <= 40 else x[:37] + "..."
    )
    df.loc[df["artifact_name"].str.len() == 40, "product_label"] = df["artifact_name"]

    fig = px.bar(
        df,
        y="product_label",
        x="repo_count",
        color="artifact_type",  # Back to artifact_type
        orientation="h",
        text="repo_count",
        custom_data=["artifact_name"],
        labels={
            "product_label": "",
            "repo_count": "Repository Count",
            "artifact_type": "Artifact Type"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Type: %{marker.color}<br>"
            "Repositories: %{x}<br>"
            "<extra></extra>"
        )
    )

    fig.update_layout(barmode="stack")
    fig.update_yaxes(automargin=True, tickfont=dict(size=12))

    return fig


def render_dependency_detection_chart(df):

    heatmap_data = df.pivot_table(
        index="classification_label",
        columns="status",
        values="repo_count",
        aggfunc="sum",
        fill_value=0
    )

    z = heatmap_data.values
    x = heatmap_data.columns.tolist()
    y = heatmap_data.index.tolist()
    text = np.vectorize(str)(z)

    fig = go.Figure(go.Heatmap(
        z=z,
        x=x,
        y=y,
        text=text,
        texttemplate="%{text}",
        textfont={"size": 12},
        colorscale=NEUTRAL_COLOR_SEQUENCE,
        showscale=False
    ))

    fig.update_layout(
        xaxis_title="",
        yaxis_title="Repo size",
        margin=dict(l=20, r=20, t=20, b=20)
    )

    return fig


from plotly import express as px
from components.chart_style import standard_chart_style

@standard_chart_style
def render_middleware_subcategory_chart(df):
    fig = px.bar(
        df,
        x="framework",
        y="repo_count",
        color="main_language",
        text="repo_count",
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        labels={
            "framework": "Framework",
            "repo_count": "Repository Count",
            "main_language": "Language"
        },
    )

    fig.update_traces(
        texttemplate="%{text}",
        textposition="inside",
        textfont_size=12
    )

    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title=None,
        yaxis_title="Repository Count",
        xaxis_tickangle=-45
    )
    fig.update_xaxes(showticklabels=True)
    return fig