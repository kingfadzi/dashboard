from components.chart_style import standard_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE
import plotly.express as px

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


def render_dependency_volume_chart(df):
    fig = px.bar(
        df,
        x="dep_bucket",
        y="repo_count",
        labels={"dep_bucket": "Dependency Count", "repo_count": "Repository Count"},
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










def render_iac_adoption_by_framework_count_chart(df):
    fig = px.bar(
        df,
        x="framework_bucket",
        y="repo_count",
        labels={
            "framework_bucket": "Frameworks Used per Repo",
            "repo_count": "Repository Count",
        },
    )
    fig.update_layout(
        xaxis_title="Frameworks Used per Repository",
        showlegend=False
    )
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




