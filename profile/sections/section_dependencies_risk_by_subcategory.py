import pandas as pd
from dash import html, dash_table
import dash_bootstrap_components as dbc

def render(profile_data):
    """
    Renders Dependency Risk Summary by Subcategory with badges.
    """

    dependencies = profile_data.get('Dependencies', [])

    if not dependencies:
        return dbc.Card(
            dbc.CardBody([
                html.H4('Dependency Risk Summary by Subcategory', className='card-title mb-4'),
                html.P("No dependency data available.", className="text-muted")
            ]),
            className="mb-4 shadow-sm"
        )

    # Convert to DataFrame
    deps_df = pd.DataFrame(dependencies)

    # Group by subcategory
    summary_df = (
        deps_df.groupby('sub_category')
        .agg(total_packages=('name', 'count'))
        .reset_index()
        .sort_values(by='total_packages', ascending=False)
    )

    # Simulate vulnerabilities per subcategory (until we have real scan data)
    summary_df['vulnerable_packages'] = [1 if i % 2 == 0 else 0 for i in range(len(summary_df))]
    summary_df['critical_vulnerabilities'] = [1 if i == 0 else 0 for i in range(len(summary_df))]

    # Build table data with badges
    table_data = []
    for _, row in summary_df.iterrows():
        table_data.append({
            "Subcategory": row['sub_category'],
            "Packages": row['total_packages'],
            "Vulnerable Packages": badge(row['vulnerable_packages'], danger_if_gt=0),
            "Critical Vulns": badge(row['critical_vulnerabilities'], danger_if_gt=0),
        })

    return dbc.Card(
        dbc.CardBody([
            html.H4('Dependency Risk Summary by Subcategory', className='card-title mb-4'),

            dash_table.DataTable(
                data=table_data,
                columns=[
                    {"name": "Subcategory", "id": "Subcategory", "presentation": "markdown"},
                    {"name": "Packages", "id": "Packages"},
                    {"name": "Vulnerable Packages", "id": "Vulnerable Packages", "presentation": "markdown"},
                    {"name": "Critical Vulns", "id": "Critical Vulns", "presentation": "markdown"},
                ],
                style_cell={
                    "fontSize": "0.8rem",
                    "padding": "5px",
                    "textAlign": "left",
                },
                style_as_list_view=True,
                style_table={"overflowX": "auto"},
                style_header={
                    "backgroundColor": "rgb(240,240,240)",
                    "fontWeight": "bold"
                },
            )
        ]),
        className="mb-4 shadow-sm"
    )

def badge(value, danger_if_gt=0):
    """
    Returns markdown for badge depending on the value.
    """
    color = "secondary"
    if value > danger_if_gt:
        color = "danger"
    elif value > 0:
        color = "warning"
    return f"![badge](https://img.shields.io/badge/{value}-{color})"