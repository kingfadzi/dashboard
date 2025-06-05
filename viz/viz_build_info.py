import plotly.express as px
import plotly.graph_objects as go
import plotly.graph_objects as go
import numpy as np
from sqlalchemy.dialects.mssql.information_schema import columns

from components.chart_style import standard_chart_style, status_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE
import pandas as pd


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

    fig.update_yaxes(
        tickformat="d"
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
def render_runtime_build_heatmap(df):
    # 1) Define your canonical order
    full_language_order = [
        "no_language",
        "markup_or_data",
        "other_programming",
        "dotnet",
        "go",
        "javascript",
        "python",
        "java",
    ]
    full_status_order = ["Only Build Tool", "Both Detected", "Only Runtime", "None Detected"]

    # 2) Pivot
    heatmap_data = df.pivot_table(
        index="language_group",
        columns="detection_status",
        values="repo_count",
        aggfunc="sum",
        fill_value=0,
    )

    # 3) Intersect with what actually exists
    existing_languages = [lang for lang in full_language_order if lang in heatmap_data.index]
    existing_statuses  = [st  for st  in full_status_order  if st  in heatmap_data.columns]

    # 4) Reindex only on the intersection (fills missing combos with 0)
    heatmap_data = heatmap_data.reindex(
        index=existing_languages,
        columns=existing_statuses,
        fill_value=0
    )

    # 5) Now extract z/x/y and force integer labels
    z = heatmap_data.values
    x = heatmap_data.columns.tolist()
    y = heatmap_data.index.tolist()
    text = np.vectorize(lambda v: str(int(v)))(z)

    # 6) Build the figure
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
        xaxis_title="Build Tool/Runtime Detection Status",
        yaxis_title="Language Group",
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
        labels={
            "variant": "Build Tool Variant",
            "repo_count": "Repository Count"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )

    fig.update_traces(
        texttemplate="%{text}",
        textposition="inside",
        textangle=0,
        textfont_size=12
    )
    fig.update_xaxes(showticklabels=True, title=None)
    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Repositories",
        margin=dict(l=20, r=20, t=20, b=20)
    )

    return fig

def render_no_buildtool_scatter(df: pd.DataFrame):
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No data available",
            xaxis=dict(title="File Count", visible=True),
            yaxis=dict(title="Repo Size (MB)", visible=True),
            margin=dict(l=20, r=20, t=40, b=20),
        )
        return fig

    fig = px.scatter(
        df,
        x="dominant_file_count",
        y="repo_size_mb",
        color="dominant_language_type",
        size="total_commits",
        hover_name="repo_id",
        hover_data=["contributor_count"],
        labels={
            "dominant_file_count": "File Count",
            "repo_size_mb": "Repo Size (MB)",
            "dominant_language_type": "Language Type",
            "total_commits": "Commits",
            "contributor_count": "Contributors"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
    )

    fig.update_traces(
        marker=dict(
            sizemode="area",
            line=dict(width=0.5, color="DarkSlateGrey")
        )
    )

    fig.update_layout(
        xaxis_title="File Count",
        yaxis_title="Repository Size (MB)",
        legend_title="Language Type",
        margin=dict(l=20, r=20, t=20, b=20),
        dragmode="zoom",  # Explicit interactive mode
    )

    return fig


def render_no_buildtool_language_type_distribution(df: pd.DataFrame):

    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No data available",
            xaxis=dict(title="Language", visible=True),
            yaxis=dict(title="Repository Count", visible=True),
            margin=dict(l=20, r=20, t=40, b=20),
        )
        return fig


    fig = px.bar(
        df,
        x="dominant_language",
        y="repo_count",
        color="classification_label",
        labels={
            "dominant_language": "Language",
            "repo_count": "Repository Count",
            "classification_label": "Size"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )


    totals = df.groupby("dominant_language")["repo_count"].sum().reset_index()

    fig.add_trace(
        go.Scatter(
            x=totals["dominant_language"],
            y=totals["repo_count"],
            mode="text",
            text=totals["repo_count"].astype(str),
            textposition="top center",
            showlegend=False
        )
    )


    fig.update_layout(
        xaxis_title="Language",
        yaxis_title="Repository Count",
        xaxis=dict(type="category", showticklabels=True, tickangle=-45),
        margin=dict(l=20, r=20, t=20, b=20),
    )

    return fig

def render_dotnet_support_status_chart(df):
    df["support_status_verbose"] = df["support_status"].map({
        "Active Support": "Active Support (.NET 8, .NET 9, .NET Framework 4.8.1)",
        "Maintenance Mode": "Maintenance Mode (.NET Framework 4.8)",
        "Out of Support": "Out of Support (5–7, Core 2.x/3.x, Fx 4.0–4.7.2)",
        "Deprecated": "Deprecated (.NET Standard 1.x–2.1)",
        "Unknown": "Unknown"
    })
    return render_support_status_chart(df)


def render_java_support_status_chart(df):
    df["support_status_verbose"] = df["support_status"].map({
        "Active Support": "Active Support (JDK 17, JDK 21)",
        "Maintenance Mode": "Maintenance Mode (JDK 11)",
        "Out of Support": "Out of Support (JDK 8)",
        "Deprecated": "Deprecated (< JDK 8)",
        "Unknown": "Unknown"
    })

    return render_support_status_chart(df)

def render_python_support_status_chart(df):
    df["support_status_verbose"] = df["support_status"].map({
        "Active Support":    "Active Support (3.11, 3.12)",
        "Maintenance Mode":  "Maintenance Mode (3.10)",
        "Out of Support":    "Out of Support (3.9)",
        "Deprecated":        "Deprecated (< 3.9)",
        "Unknown":           "Unknown"
    })

    watermark_text = "Detection for Python versions may be incomplete."
    return render_support_status_chart(df, watermark_text=watermark_text)


def render_js_support_status_chart(df):
    df["support_status_verbose"] = df["support_status"].map({
        "Active Support": "Active Support (Node 18, 20)",
        "Maintenance Mode": "Maintenance Mode (Node 16)",
        "Out of Support": "Out of Support (Node 14)",
        "Deprecated": "Deprecated (< Node 14)",
        "Unknown": "Unknown"
    })

    watermark_text = "Detection for Javascript versions may be incomplete."
    return render_support_status_chart(df, watermark_text=watermark_text)


def render_go_support_status_chart(df):
    df["support_status_verbose"] = df["support_status"].map({
        "Active Support": "Active Support (Go 1.20–1.22)",
        "Maintenance Mode": "Maintenance Mode (Go 1.19)",
        "Out of Support": "Out of Support (Go 1.18)",
        "Deprecated": "Deprecated (< Go 1.18)",
        "Unknown": "Unknown"
    })

    return render_support_status_chart(df)

@status_chart_style
def render_support_status_chart(
        df: pd.DataFrame,
        annotation_text: str = None,
        watermark_text: str = None
) -> go.Figure:

    # Decide which column to use for hover (verbose if present)
    hover_name = "support_status_verbose" if "support_status_verbose" in df.columns else "support_status"

    # 1) Create the base horizontal stacked bar chart
    fig = px.bar(
        df,
        x="repo_count",
        y="support_status",
        color="classification_label",
        orientation="h",
        hover_name=hover_name,
        labels={
            "support_status": "",
            "repo_count": "Repository Count",
            "classification_label": "Size"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )

    # 2) Remove any automatically drawn text labels on the individual bar segments
    fig.update_traces(
        selector=dict(type="bar"),
        text=None,
        textposition=None
    )

    # 3) Add exactly one “total” annotation per bar using a Scatter trace
    totals = df.groupby("support_status", as_index=False)["repo_count"].sum()
    for _, row in totals.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[row["repo_count"]],
                y=[row["support_status"]],
                mode="text",
                text=[str(row["repo_count"])],
                textposition="middle right",
                showlegend=False,
                textfont=dict(size=12, color="black")
            )
        )

    # 4) If watermark_text is provided, add it on top as faint centered text
    if watermark_text:
        fig.add_annotation(
            text=watermark_text,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=11, color="white"),
            xanchor="center",
            yanchor="middle",
            textangle=-30        # diagonal for watermark effect

        )

    # 5) If annotation_text is provided, place it as a caption below the x-axis
    if annotation_text:
        fig.add_annotation(
            text=annotation_text,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.15,
            showarrow=False,
            align="left",
            font=dict(size=11, color="black"),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#cccccc",
            borderwidth=1
        )

    return fig
