from dash import Output, Input
from data.code_insights_lizard_fetchers import (
    fetch_total_ccn_buckets,
    fetch_function_count_buckets,
    fetch_total_nloc_buckets,
    fetch_ccn_vs_function_count,
)
from viz.viz_code_insights_lizard import (
    render_total_ccn_chart,
    render_function_count_chart,
    render_total_nloc_chart,
    render_ccn_vs_function_count_chart,
)

def register_code_insights_lizard_callbacks(app):
    @app.callback(
        Output("total-ccn-chart", "figure"),
        Input("host-name-filter", "value"),
        Input("app-id-filter", "value"),
        Input("tc-filter", "value"),
        Input("language-filter", "value"),
        Input("classification-filter", "value"),
        Input("activity-status-filter", "value")
    )
    def update_total_ccn_chart(hosts, apps, tcs, languages, classifications, activity):
        filters = {
            "host_name": hosts,
            "app_id": apps,
            "tc": tcs,
            "main_language": languages,
            "classification_label": classifications,
            "activity_status": activity,
        }
        df = fetch_total_ccn_buckets(filters)
        return render_total_ccn_chart(df)

    @app.callback(
        Output("function-count-chart", "figure"),
        Input("host-name-filter", "value"),
        Input("app-id-filter", "value"),
        Input("tc-filter", "value"),
        Input("language-filter", "value"),
        Input("classification-filter", "value"),
        Input("activity-status-filter", "value")
    )
    def update_function_count_chart(hosts, apps, tcs, languages, classifications, activity):
        filters = {
            "host_name": hosts,
            "app_id": apps,
            "tc": tcs,
            "main_language": languages,
            "classification_label": classifications,
            "activity_status": activity,
        }
        df = fetch_function_count_buckets(filters)
        return render_function_count_chart(df)

    @app.callback(
        Output("total-nloc-chart", "figure"),
        Input("host-name-filter", "value"),
        Input("app-id-filter", "value"),
        Input("tc-filter", "value"),
        Input("language-filter", "value"),
        Input("classification-filter", "value"),
        Input("activity-status-filter", "value")
    )
    def update_total_nloc_chart(hosts, apps, tcs, languages, classifications, activity):
        filters = {
            "host_name": hosts,
            "app_id": apps,
            "tc": tcs,
            "main_language": languages,
            "classification_label": classifications,
            "activity_status": activity,
        }
        df = fetch_total_nloc_buckets(filters)
        return render_total_nloc_chart(df)

    @app.callback(
        Output("ccn-vs-function-count-chart", "figure"),
        Input("host-name-filter", "value"),
        Input("app-id-filter", "value"),
        Input("tc-filter", "value"),
        Input("language-filter", "value"),
        Input("classification-filter", "value"),
        Input("activity-status-filter", "value")
    )
    def update_ccn_vs_function_count_chart(hosts, apps, tcs, languages, classifications, activity):
        filters = {
            "host_name": hosts,
            "app_id": apps,
            "tc": tcs,
            "main_language": languages,
            "classification_label": classifications,
            "activity_status": activity,
        }
        df = fetch_ccn_vs_function_count(filters)
        return render_ccn_vs_function_count_chart(df)
