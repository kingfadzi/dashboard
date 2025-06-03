import plotly.express as px
import plotly.graph_objects as go
import plotly.graph_objects as go
import numpy as np

from components.chart_style import standard_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE


# 1. Detection Coverage by Tool
@standard_chart_style
def render_detection_coverage_chart(df):
    fig = go.Figure()

    statuses = df["detection_status"].unique()
    tools = sorted(df["tool"].unique())

    for i, status in enumerate(statuses):
        filtered = df[df["detection_status"] == status]
        visible = "legendonly" if status == "No Modules Detected" else True
        fig.add_trace(go.Bar(
            x=filtered["tool"],
            y=filtered["repo_count"],
            name=status,
            visible=visible,
            text=filtered["repo_count"],
            texttemplate="%{text}",
            textposition="inside",
            marker_color=NEUTRAL_COLOR_SEQUENCE[i % len(NEUTRAL_COLOR_SEQUENCE)]
        ))

    fig.update_layout(
        barmode="stack",
        xaxis_title=None,
        yaxis_title="Repository Count",
        title=None,
        margin=dict(l=20, r=20, t=20, b=20),
        uniformtext_minsize=8,
        uniformtext_mode="hide"
    )
    fig.update_xaxes(showticklabels=True)

    return fig

@standard_chart_style
def render_module_count_chart(df):
    fig = px.bar(
        df,
        x="module_bucket",
        y="repo_count",
        color="classification_label",
        text="repo_count",
        labels={
            "module_bucket": "Module Count Range",
            "repo_count": "Repository Count",
            "classification_label": "Classification"
        },
        barmode="stack"
    )

    fig.update_traces(
        texttemplate="%{text}",
        textposition="inside",
        textfont_size=12
    )

    fig.update_layout(
        title=None,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    fig.update_xaxes(showticklabels=True)

    return fig

# 3. Repos per Tool and Variant
def render_repos_per_tool_variant_chart(df):
    fig = px.bar(
        df,
        x="variant",
        y="repo_count",
        color="tool",
        barmode="group",
        labels={"variant": "Build Tool Variant", "tool": "Language Tool", "repo_count": "Repository Count"},
    )
    fig.update_xaxes(tickangle=45)
    fig.update_layout(title=None)
    return fig

from components.colors import NEUTRAL_COLOR_SEQUENCE

# 4. Status by Tool
@standard_chart_style
def render_status_by_tool_chart(df):
    fig = px.bar(
        df,
        x="tool",
        y="repo_count",
        text="repo_count",
        color="status",
        barmode="stack",
        labels={
            "tool": "",
            "status": "Status",
            "repo_count": "Repository Count"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
    )
    fig.update_xaxes(showticklabels=True)
    fig.update_layout(title=None)
    return fig


@standard_chart_style
def render_runtime_versions_chart(df):
    df = df.sort_values("repo_count", ascending=False)

    fig = px.bar(
        df,
        x="runtime_version",
        y="repo_count",
        color="variant",
        barmode="stack",
        labels={
            "runtime_version": "",
            "variant": "Build Tool Variant",
            "repo_count": "Repository Count"
        },
        text="repo_count",
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )

    fig.update_traces(
        texttemplate="%{text}",
        textposition="inside",
        textangle=0,
        textfont_size=12
    )

    fig.update_xaxes(
        showticklabels=True,
        tickangle=45,
        title=None
    )

    fig.update_layout(
        title=None,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    return fig


# 6. Runtime Fragmentation by Tool
@standard_chart_style
def render_runtime_fragmentation_chart(df):
    fig = px.bar(
        df,
        text="version_count",
        x="tool",
        y="version_count",
        labels={
            "tool": "",
            "version_count": "Distinct Runtime Versions"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        title=None,
        xaxis_tickangle=-45,
        xaxis_tickfont=dict(size=10),
    )
    fig.update_xaxes(showticklabels=True)
    return fig


@standard_chart_style
def render_confidence_distribution_chart(df):
    df["tool"] = df["tool"].fillna("unknown")

    tool_order = (
        df.groupby("tool")["repo_count"]
        .sum()
        .sort_values(ascending=False)
        .index.tolist()
    )

    fig = px.bar(
        df,
        x="confidence",
        y="repo_count",
        color="tool",
        category_orders={"tool": tool_order},
        barmode="stack",
        labels={
            "confidence": "Confidence Level",
            "repo_count": "Repository Count",
            "tool": "Build Tool"
        },
        text="repo_count",
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )

    fig.update_traces(
        texttemplate="%{text}",
        textposition="inside",
        textfont_size=12
    )

    fig.update_xaxes(
        showticklabels=True,
        categoryorder="array",
        categoryarray=["high", "medium", "low", "unknown"]
    )

    fig.update_layout(
        title=None,
        uniformtext_minsize=8,
        uniformtext_mode="hide",
        margin=dict(l=20, r=20, t=20, b=20)
    )

    return fig



# 8. Runtime Coverage Heatmap
def render_runtime_coverage_heatmap(df):
    # Pivot: tool on Y-axis, runtime_status on X-axis
    heatmap_data = df.pivot_table(
        index="tool",
        columns="runtime_status",
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
        yaxis_title="",
        margin=dict(l=20, r=20, t=20, b=20)
    )

    return fig


@standard_chart_style
def render_build_tool_variant_chart(df):
    fig = px.bar(
        df,
        x="variant",
        y="repo_count",
        text="repo_count",
        color="runtime_version",
        labels={
            "repo_count": "Repository Count",
            "runtime_version": "Runtime Version"
        },
        barmode="stack",
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )

    fig.update_traces(
        texttemplate="%{text}",
        textposition="inside",
        textangle=0,
        textfont_size=12
    )
    fig.update_xaxes(showticklabels=True, title=None)  # Ensure title is suppressed
    fig.update_layout(
        xaxis_title=None,  # Explicitly remove x-axis title
        yaxis_title="Repositories",
        legend_title="Runtime",
        margin=dict(l=20, r=20, t=20, b=20)
    )

    return fig


