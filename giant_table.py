import pandas as pd
from dash import Dash, dcc, html, dash_table, Input, Output

# Simulate data
row_count = 20
df = pd.DataFrame([{
    "repo_id": f"repo_{i}",
    "source_code_file_count": i * 10,
    "total_blank": i * 5,
    "total_comment": i * 3,
    "total_lines_of_code": i * 100,
    "total_trivy_vulns": i,
    "trivy_critical": i % 5,
    "trivy_high": i % 4,
    "trivy_medium": i % 6,
    "trivy_low": i % 2,
    "total_semgrep_findings": i * 2,
    "cat_best_practice": i,
    "cat_compatibility": i,
    "cat_correctness": i,
    "cat_maintainability": i,
    "cat_performance": i,
    "cat_portability": i,
    "cat_security": i,
    "main_language": "Python",
    "all_languages": "Python,JavaScript",
    "classification_label": "Internal",
    "app_id": f"app_{i}",
    "repo_size_bytes": i * 1000,
    "component_id": f"comp_{i}",
    "component_name": f"Component {i}",
    "web_url": f"https://repo{i}.git",
    "transaction_cycle": "Quarterly",
    "business_application_name": f"BusinessApp {i}",
    "tech_lead_group": "TechGroup",
    "correlation_id": f"corr-{i}",
    "active": "Y",
    "owning_transaction_cycle": "Quarterly",
    "resilience_category": "High",
    "application_product_owner": "Owner A",
    "application_product_owner_brid": "brid123",
    "system_architect": "Architect A",
    "system_architect_brid": "brid321",
    "operational_status": "Live",
    "application_type": "Web",
    "architecture_type": "Microservices",
    "install_type": "Docker",
    "application_tier": "App",
    "architecture_hosting": "Cloud",
    "house_position": "Top",
    "business_application_sys_id": f"sys{i}",
    "short_description": "A test repo",
    "chief_technology_officer": "CTO Name",
    "business_owner": "Owner B",
    "business_owner_brid": "brid456"
} for i in range(row_count)])

# Logical column groups
column_groups = {
    "Code Metrics": [
        "source_code_file_count", "total_blank", "total_comment", "total_lines_of_code"
    ],
    "Vulnerability - Trivy": [
        "total_trivy_vulns", "trivy_critical", "trivy_high", "trivy_medium", "trivy_low"
    ],
    "Vulnerability - Semgrep": [
        "total_semgrep_findings", "cat_best_practice", "cat_compatibility",
        "cat_correctness", "cat_maintainability", "cat_performance", "cat_portability", "cat_security"
    ],
    "Repository Info": [
        "repo_id", "main_language", "all_languages", "classification_label", "app_id",
        "repo_size_bytes", "component_id", "component_name", "web_url", "transaction_cycle"
    ],
    "App Metadata": [
        "business_application_name", "tech_lead_group", "correlation_id", "active",
        "owning_transaction_cycle", "resilience_category", "application_product_owner",
        "application_product_owner_brid", "system_architect", "system_architect_brid",
        "operational_status", "application_type", "architecture_type", "install_type",
        "application_tier", "architecture_hosting", "house_position", "business_application_sys_id",
        "short_description", "chief_technology_officer", "business_owner", "business_owner_brid"
    ]
}

app = Dash(__name__)
app.title = "Wide Table Viewer"

app.layout = html.Div([
    html.H3("Repository Catalog Viewer"),
    dcc.Tabs(
        id="column-group-tabs",
        value="Code Metrics",
        children=[dcc.Tab(label=group, value=group) for group in column_groups]
    ),
    dash_table.DataTable(
        id="wide-table",
        data=[],
        columns=[],
        page_size=10,
        style_table={"overflowX": "auto"},
        fixed_rows={"headers": True},
    )
])

@app.callback(
    Output("wide-table", "columns"),
    Output("wide-table", "data"),
    Input("column-group-tabs", "value")
)
def update_columns(tab_name):
    cols = column_groups[tab_name]
    return [{"name": c, "id": c} for c in cols], df[cols].to_dict("records")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)