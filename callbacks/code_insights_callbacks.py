from dash import Input, Output
from app import app
from fetchers.code_insights_fetchers import fetch_role_distribution, fetch_normalized_weight
from viz.viz_code_insights_charts import render_role_distribution_chart, render_normalized_weight_chart

@app.callback(
    Output("role-distribution-chart", "figure"),
    Input("host-name-filter", "value"),
    Input("app-id-filter", "value"),
    Input("tc-filter", "value"),
    Input("language-filter", "value"),
    Input("classification-filter", "value"),
    Input("activity-status-filter", "value")
)
def update_role_distribution(hosts, apps, tcs, languages, classifications, activity):
    filters = {
        "hosts": hosts,
        "apps": apps,
        "tcs": tcs,
        "languages": languages,
        "classifications": classifications,
        "activity_status": activity
    }
    df = fetch_role_distribution(filters)
    return render_role_distribution_chart(df).figure


@app.callback(
    Output("normalized-weight-chart", "figure"),
    Input("host-name-filter", "value"),
    Input("app-id-filter", "value"),
    Input("tc-filter", "value"),
    Input("language-filter", "value"),
    Input("classification-filter", "value"),
    Input("activity-status-filter", "value")
)
def update_normalized_weight(hosts, apps, tcs, languages, classifications, activity):
    filters = {
        "hosts": hosts,
        "apps": apps,
        "tcs": tcs,
        "languages": languages,
        "classifications": classifications,
        "activity_status": activity
    }
    df = fetch_normalized_weight(filters)
    return render_normalized_weight_chart(df).figure
