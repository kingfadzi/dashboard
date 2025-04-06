import plotly.graph_objects as go
import pandas as pd
import datetime

def create_health_chart(health_scores):
    categories = list(health_scores.keys())
    scores = list(health_scores.values())
    fig = go.Figure(go.Bar(
        x=scores,
        y=categories,
        orientation='h',
        marker_color=['green' if s > 70 else 'orange' if s > 50 else 'red' for s in scores]
    ))
    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        height=300,
        title="",
        xaxis=dict(range=[0, 100]),
        showlegend=False,
    )
    return fig

def create_language_pie(language_data):
    labels = list(language_data.keys())
    values = list(language_data.values())
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.3,
        textinfo='percent+label',
        insidetextorientation='radial'
    )])
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        showlegend=False
    )
    return fig

def create_commit_sparkline(commits):
    months = pd.date_range(end=datetime.date.today(), periods=12, freq='M').strftime('%b').tolist()
    fig = go.Figure(go.Scatter(x=months, y=commits, mode='lines+markers'))
    fig.update_layout(
        title="",
        height=250,
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=False,
    )
    return fig

def create_dependency_category_bar(dependencies_df):
    category_counts = dependencies_df['category'].value_counts()
    fig = go.Figure(go.Bar(
        y=category_counts.index,
        x=category_counts.values,
        orientation='h',
        text=category_counts.values,
        textposition='auto'
    ))
    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        height=300,
        xaxis_title="Dependencies",
        yaxis_title="Category",
        showlegend=False,
    )
    return fig

def get_top_subcategories_age(dependencies_df):
    return (
        dependencies_df
        .groupby('sub_category')
        .agg(
            packages=('name', 'count'),
            avg_age=('age', 'mean')
        )
        .sort_values(by='packages', ascending=False)
        .reset_index()
        .head(5)
    )

def get_top_oldest_dependencies(dependencies_df):
    return dependencies_df.sort_values(by='age', ascending=False).head(5)