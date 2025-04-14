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

def create_language_bar(language_data):
    if not language_data:
        return go.Figure()

    sorted_items = sorted(language_data.items(), key=lambda item: item[1], reverse=True)
    top_5 = sorted_items[:5]
    others = sorted_items[5:]

    labels = [label for label, _ in top_5]
    values = [value for _, value in top_5]

    if others:
        others_value = sum(value for _, value in others)
        if others_value > 0:
            labels.append('Others')
            values.append(others_value)

    bar_colors = [
        '#fc8d62',
        '#66c2a5',
        '#e78ac3',
        '#a6d854',
        '#ffd92f',
        '#e5c494',
        '#c7e9b4',
        '#fdb462',
    ]

    fig = go.Figure(data=[
        go.Bar(
            x=values,
            y=labels,
            orientation='h',
            marker_color=[bar_colors[i % len(bar_colors)] for i in range(len(labels))],
            text=[f"{v:.1f}%" for v in values],
            textposition='auto',
        )
    ])

    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis_title=None,
        yaxis_title=None,
        xaxis=dict(showgrid=False, zeroline=False, fixedrange=True),
        yaxis=dict(showgrid=False, zeroline=False, fixedrange=True),
        showlegend=False,
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

def calculate_dependency_risks(profile_data):
    vulnerabilities = profile_data.get('Vulnerabilities', [])
    total_deps = profile_data.get('Total Dependencies', 1)  # Protect against division by zero

    vuln_count = len(vulnerabilities)
    vuln_percentage = round((vuln_count / total_deps) * 100, 1)

    critical_or_high = sum(1 for v in vulnerabilities if v.get('severity') in ('Critical', 'High'))
    critical_or_high_percentage = round((critical_or_high / total_deps) * 100, 1)

    no_fix_vulns = sum(1 for v in vulnerabilities if not v.get('fix_version') or v.get('fix_version') in ('None', '-', ''))
    critical_no_fix = sum(1 for v in vulnerabilities if v.get('severity') == 'Critical' and (not v.get('fix_version') or v.get('fix_version') in ('None', '-', '')))

    severity_counts = {
        'Critical': 0,
        'High': 0,
        'Medium': 0,
        'Low': 0
    }
    for v in vulnerabilities:
        sev = v.get('severity')
        if sev in severity_counts:
            severity_counts[sev] += 1

    return {
        "total_dependencies": total_deps,
        "vulnerable_percentage": vuln_percentage,
        "critical_high_percentage": critical_or_high_percentage,
        "vulnerable_without_fix": no_fix_vulns,
        "critical_without_fix": critical_no_fix,
        "severity_counts": severity_counts
    }
