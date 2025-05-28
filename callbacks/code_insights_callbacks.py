from dash import Input, Output

from data.fetch_markup_language import fetch_markup_language_usage

from data.code_insights_fetchers import (
    fetch_role_distribution,
    fetch_normalized_weight
    
)
from viz.viz_code_insights_charts import (
    render_role_distribution_chart,
    render_normalized_weight_chart,
)
from viz.viz_code_insights_markup import render_markup_language_usage_chart

def register_code_insights_callbacks(app):

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
            "host_name": hosts,
            "app_id": apps,
            "transaction_cycle": tcs,
            "main_language": languages,
            "classification_label": classifications,
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
            "host_name": hosts,
            "app_id": apps,
            "transaction_cycle": tcs,
            "main_language": languages,
            "classification_label": classifications,
            "activity_status": activity
        }
        df = fetch_normalized_weight(filters)
        return render_normalized_weight_chart(df).figure

    @app.callback(
        Output("markup-language-usage-chart", "children"),
        Input("host-name-filter", "value"),
        Input("app-id-filter", "value"),
        Input("tc-filter", "value"),
        Input("language-filter", "value"),
        Input("classification-filter", "value"),
        Input("activity-status-filter", "value")
    )
    def update_markup_usage(hosts, apps, tcs, languages, classifications, activity):
        filters = {
            "host_name": hosts,
            "app_id": apps,
            "transaction_cycle": tcs,
            "main_language": languages,
            "classification_label": classifications,
            "activity_status": activity
        }
        df = fetch_markup_language_usage(filters)
        return render_markup_language_usage_chart(df)