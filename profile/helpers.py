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


def create_language_bar(language_data):
    if not language_data:
        return go.Figure()  # Empty figure fallback

    # Sort languages by usage % descending
    sorted_langs = sorted(language_data.items(), key=lambda x: x[1], reverse=True)

    # Keep top 9 languages, bundle rest as "Other"
    top_langs = sorted_langs[:9]
    if len(sorted_langs) > 9:
        others_pct = sum(pct for _, pct in sorted_langs[9:])
        top_langs.append(("Other", others_pct))

    languages = [lang for lang, _ in top_langs]
    percentages = [pct for _, pct in top_langs]

    fig = go.Figure(go.Bar(
        x=percentages,
        y=languages,
        orientation='h',
        text=[f"{p}%" for p in percentages],
        textposition='auto',
        marker_color=[
            "#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A",
            "#19D3F3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"
        ]  # Consistent neutral/cool palette, NO red/green meaning
    ))

    fig.update_layout(
        title=None,
        margin=dict(t=0, b=0, l=0, r=0),
        height=350,
        showlegend=False,
        xaxis_title='Percentage (%)',
        yaxis_title='Language',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
    )

    fig.update_layout(
        dragmode=False  # Disable zooming/panning
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