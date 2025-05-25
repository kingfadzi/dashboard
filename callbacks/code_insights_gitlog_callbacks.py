from dash import Input, Output

from data.code_insights_gitlog_fetchers import fetch_avg_file_size_buckets, fetch_contributor_dominance, \
    fetch_branch_sprawl, fetch_repo_age_buckets
from viz.viz_code_insights_gitlog import (
    render_avg_file_size_chart,
    render_contributor_dominance_chart,
    render_branch_sprawl_chart,
    render_repo_age_chart,
)

def register_code_insights_gitlog_callbacks(app):

    @app.callback(
        Output("avg-file-size-chart", "figure"),
        Input("host-name-filter", "value"),
        Input("app-id-filter", "value"),
        Input("tc-filter", "value"),
        Input("language-filter", "value"),
        Input("classification-filter", "value"),
        Input("activity-status-filter", "value")
    )
    def update_avg_file_size_chart(hosts, apps, tcs, languages, classifications, activity):
        filters = {
            "host_name": hosts,
            "app_id": apps,
            "tc": tcs,
            "main_language": languages,
            "classification_label": classifications,
            "activity_status": activity
        }
        df = fetch_avg_file_size_buckets(filters)
        return render_avg_file_size_chart(df).figure


    @app.callback(
        Output("contributor-dominance-chart", "figure"),
        Input("host-name-filter", "value"),
        Input("app-id-filter", "value"),
        Input("tc-filter", "value"),
        Input("language-filter", "value"),
        Input("classification-filter", "value"),
        Input("activity-status-filter", "value")
    )
    def update_contributor_dominance_chart(hosts, apps, tcs, languages, classifications, activity):
        filters = {
            "host_name": hosts,
            "app_id": apps,
            "tc": tcs,
            "main_language": languages,
            "classification_label": classifications,
            "activity_status": activity
        }
        df = fetch_contributor_dominance(filters)
        return render_contributor_dominance_chart(df).figure


    @app.callback(
        Output("branch-sprawl-chart", "figure"),
        Input("host-name-filter", "value"),
        Input("app-id-filter", "value"),
        Input("tc-filter", "value"),
        Input("language-filter", "value"),
        Input("classification-filter", "value"),
        Input("activity-status-filter", "value")
    )
    def update_branch_sprawl_chart(hosts, apps, tcs, languages, classifications, activity):
        filters = {
            "host_name": hosts,
            "app_id": apps,
            "tc": tcs,
            "main_language": languages,
            "classification_label": classifications,
            "activity_status": activity
        }
        df = fetch_branch_sprawl(filters)
        return render_branch_sprawl_chart(df).figure


    @app.callback(
        Output("repo-age-chart", "figure"),
        Input("host-name-filter", "value"),
        Input("app-id-filter", "value"),
        Input("tc-filter", "value"),
        Input("language-filter", "value"),
        Input("classification-filter", "value"),
        Input("activity-status-filter", "value")
    )
    def update_repo_age_chart(hosts, apps, tcs, languages, classifications, activity):
        filters = {
            "host_name": hosts,
            "app_id": apps,
            "tc": tcs,
            "main_language": languages,
            "classification_label": classifications,
            "activity_status": activity
        }
        df = fetch_repo_age_buckets(filters)
        return render_repo_age_chart(df).figure
