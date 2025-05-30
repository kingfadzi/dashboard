from dash import Input, Output
from data.fetch_table_data import fetch_table_data
from viz.viz_table_data import viz_table_data
from utils.filter_utils import extract_filter_dict_from_store


def get_table_outputs(store_data):
    filters = extract_filter_dict_from_store(store_data or {})
    df, _ = fetch_table_data(filters, 0, 1000)
    table_data = viz_table_data(df)

    column_defs = [
        {"headerName": "Repo Name", "field": "repo_id", "cellRenderer": "htmlRenderer"},
        {"headerName": "TC", "field": "tc"},
        {"headerName": "App ID", "field": "app_id", "cellRenderer": "htmlRenderer"},
        {"headerName": "Status", "field": "activity_status"},
        {"headerName": "Size", "field": "classification_label"},
        {"headerName": "Age", "field": "repo_age_days"},
        {"headerName": "Language", "field": "all_languages"},
        {"headerName": "Scope", "field": "scope"},
        {"headerName": "Commits", "field": "total_commits"},
        {"headerName": "Contributors", "field": "number_of_contributors"},
        {"headerName": "Last Commit", "field": "last_commit_date"},
    ]

    return table_data, column_defs


def register_table_callbacks(app):
    @app.callback(
        [Output("overview-table", "rowData"), Output("overview-table", "columnDefs")],
        [Input("default-filter-store", "data")],
    )
    def update_overview_table(store_data):
        return get_table_outputs(store_data)

    @app.callback(
        [Output("build-info-table", "rowData"), Output("build-info-table", "columnDefs")],
        [Input("default-filter-store", "data")],
    )
    def update_build_info_table(store_data):
        return get_table_outputs(store_data)

    @app.callback(
        [Output("code-insights-table", "rowData"), Output("code-insights-table", "columnDefs")],
        [Input("default-filter-store", "data")],
    )
    def update_code_insights_table(store_data):
        return get_table_outputs(store_data)

    @app.callback(
        [Output("dependencies-table", "rowData"), Output("dependencies-table", "columnDefs")],
        [Input("default-filter-store", "data")],
    )
    def update_dependencies_table(store_data):
        return get_table_outputs(store_data)

    @app.callback(
        Output("default-filter-store", "data", allow_duplicate=True),
        [
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
            Input("host-name-filter", "value"),
        ],
        prevent_initial_call=True,
    )
    def update_filter_store(activity, tc, lang, classification, app_id, host):
        return {
            "activity_status": activity,
            "transaction_cycle": tc,
            "main_language": lang,
            "classification_label": classification,
            "app_id": app_id,
            "host_name": host,
        }