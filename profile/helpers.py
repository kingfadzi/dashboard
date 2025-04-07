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


import plotly.graph_objects as go

import plotly.graph_objects as go

def create_language_bar(language_data):
    # Sort and limit to top 10 languages
    sorted_items = sorted(language_data.items(), key=lambda x: x[1], reverse=True)
    top_languages = dict(sorted_items[:10])

    # If more than 10, bundle the rest into 'Other'
    if len(sorted_items) > 10:
        other_total = sum([v for k, v in sorted_items[10:]])
        top_languages['Other'] = round(other_total, 2)

    fig = go.Figure(go.Bar(
        y=list(top_languages.keys()),
        x=list(top_languages.values()),
        orientation='h',
        text=[f"{v}%" for v in top_languages.values()],
        textposition='auto',
    ))

    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        height=300,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            title=None,
            showgrid=True,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            title=None,
            showgrid=False,
            zeroline=False,
        )
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
    
    
def classify_avg_ccn(avg_ccn):
    if avg_ccn < 4:
        return "Good"
    elif avg_ccn <= 6:
        return "Moderate"
    else:
        return "High Risk"

def classify_comment_quality(comment_percent):
    if comment_percent >= 15:
        return "Excellent"
    elif comment_percent >= 8:
        return "Moderate"
    else:
        return "Poor"

def classify_function_density(total_functions):
    if total_functions < 500:
        return "Small Codebase"
    elif total_functions <= 2000:
        return "Medium Codebase"
    else:
        return "Large Codebase"

def classify_total_ccn(total_ccn):
    if total_ccn < 1500:
        return "Low Risk"
    elif total_ccn <= 3000:
        return "Medium Risk"
    else:
        return "High Risk"
        

def create_dependency_category_bar(dependencies_df):
    category_counts = dependencies_df['category'].value_counts().sort_values()
    
    fig = go.Figure(go.Bar(
        x=category_counts.values,
        y=category_counts.index,
        orientation='h',
        marker_color='rgb(30,144,255)',
        text=category_counts.values,
        textposition='outside',
        hoverinfo='y+x',
    ))

    fig.update_layout(
        margin=dict(t=20, b=20, l=40, r=10),
        height=300,
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(200,200,200,0.2)',
            zeroline=False
        ),
        yaxis=dict(
            showgrid=False
        ),
        showlegend=False
    )
    return fig