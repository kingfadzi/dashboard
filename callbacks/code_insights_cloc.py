from dash import Input, Output
from data.code_insights_cloc_fetchers import (
    fetch_code_volume_by_language,
    fetch_file_count_by_language,
    fetch_code_composition_by_language,
    fetch_code_file_scatter,
)
from viz.viz_code_insights_cloc import (
    render_code_volume_chart,
    render_file_count_chart,
    render_code_composition_chart,
    render_code_file_scatter_chart,
)

def register_code_insights_cloc_callbacks(app):

    @app.callback(
        Output("code-volume-chart", "figure"),
        Input("host-name-filter", "value"),
        Input("app-id-filter", "value"),
        Input("tc-filter", "value"),
        Input("language-filter", "value"),
        Input("classification-filter", "value"),
        Input("activity-status-filter", "value")
    )
    def update_code_volume_chart(hosts, apps, tcs, languages, classifications, activity):
        filters = {
            "host_name": hosts,
            "app_id": apps,
            "tc": tcs,
            "main_language": languages,
            "classification_label": classifications,
            "activity_status": activity
        }
        df = fetch_code_volume_by_language(filters)
        return render_code_volume_chart(df).figure

    @app.callback(
        Output("file-count-chart", "figure"),
        Input("host-name-filter", "value"),
        Input("app-id-filter", "value"),
        Input("tc-filter", "value"),
        Input("language-filter", "value"),
        Input("classification-filter", "value"),
        Input("activity-status-filter", "value")
    )
    def update_file_count_chart(hosts, apps, tcs, languages, classifications, activity):
        filters = {
            "host_name": hosts,
            "app_id": apps,
            "tc": tcs,
            "main_language": languages,
            "classification_label": classifications,
            "activity_status": activity
        }
        df = fetch_file_count_by_language(filters)
        return render_file_count_chart(df).figure

    @app.callback(
        Output("code-composition-chart", "figure"),
        Input("host-name-filter", "value"),
        Input("app-id-filter", "value"),
        Input("tc-filter", "value"),
        Input("language-filter", "value"),
        Input("classification-filter", "value"),
        Input("activity-status-filter", "value")
    )
    def update_code_composition_chart(hosts, apps, tcs, languages, classifications, activity):
        filters = {
            "host_name": hosts,
            "app_id": apps,
            "tc": tcs,
            "main_language": languages,
            "classification_label": classifications,
            "activity_status": activity
        }
        df = fetch_code_composition_by_language(filters)
        return render_code_composition_chart(df).figure

    @app.callback(
        Output("code-file-scatter-chart", "figure"),
        Input("host-name-filter", "value"),
        Input("app-id-filter", "value"),
        Input("tc-filter", "value"),
        Input("language-filter", "value"),
        Input("classification-filter", "value"),
        Input("activity-status-filter", "value")
    )
    def update_code_file_scatter_chart(hosts, apps, tcs, languages, classifications, activity):
        filters = {
            "host_name": hosts,
            "app_id": apps,
            "tc": tcs,
            "main_language": languages,
            "classification_label": classifications,
            "activity_status": activity
        }
        df = fetch_code_file_scatter(filters)
        return render_code_file_scatter_chart(df).figure
