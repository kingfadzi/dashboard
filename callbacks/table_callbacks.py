# table_callbacks.py

from dash import Input, Output, callback, State
import urllib.parse

from dash.exceptions import PreventUpdate

from data.fetch_table_data import fetch_table_data

def get_table_outputs_from_store(store_data, table_id=None):
    filters = { k: v for k, v in (store_data or {}).items() if v not in (None, "") }
    df, _ = fetch_table_data(filters, 0, 1000)
    table_data = df.to_dict("records")

    # Build a “returnUrl” for any link in the table (optional)
    return_url = f"/table-{table_id}"
    encoded_return_url = urllib.parse.quote(return_url)

    column_defs = [
        {
            "headerName": "Repo Name",
            "field": "repo_id",
            "cellRenderer": "markdown",
            "valueGetter": {
                "function": (
                    f"`[${'{'}params.data.repo_id{'}'}]("
                    f"/repo?repo_id=${'{'}params.data.repo_id{'}'}&returnUrl={encoded_return_url})`"
                )
            },
            "filterValueGetter": {"function": "params.data.repo_id"},
            "cellRendererParams": {"linkTarget": "_self", "html": True},
        },
        {
            "headerName": "App ID",
            "field": "app_id",
            "cellRenderer": "markdown",
            "valueGetter": {
                "function": (
                    f"`[${'{'}params.data.app_id{'}'}](${ '{' }params.data.browse_url{'}'})`"
                )
            },
            "filterValueGetter": {"function": "params.data.app_id"},
            "cellRendererParams": {"linkTarget": "_blank", "html": True},
        },
        {"headerName": "Status", "field": "activity_status"},
        {"headerName": "Size", "field": "classification_label"},
        {"headerName": "Age", "field": "repo_age_days", "type": "numericColumn"},
        {"headerName": "Language", "field": "all_languages"},
        {"headerName": "Scope", "field": "scope"},
        {"headerName": "Commits", "field": "total_commits", "type": "numericColumn"},
        {"headerName": "Contributors", "field": "number_of_contributors", "type": "numericColumn"},
        {
            "headerName": "Last Commit",
            "field": "last_commit_date",
            "valueFormatter": {
                "function": "params.value ? new Date(params.value).toLocaleDateString() : ''"
            },
        },
    ]

    return table_data, column_defs


def register_table_callbacks(app):
    # For each of the four “table” pages, only run when pathname matches
    for table_id in ["overview", "build-info", "code-insights", "dependencies"]:
        @app.callback(
            Output(f"{table_id}-table", "rowData"),
            Output(f"{table_id}-table", "columnDefs"),
            Input("default-filter-store", "data"),
            State("url", "pathname"),
        )
        def update_table(store_data, pathname, table_id=table_id):
            if not pathname.startswith(f"/table-{table_id}"):
                raise PreventUpdate

            table_data, column_defs = get_table_outputs_from_store(store_data, table_id=table_id)
            return table_data, column_defs

    # Build each “Table” button’s href from the current dropdown values
    for table_id in ["overview", "build-info", "code-insights", "dependencies"]:
        @app.callback(
            Output(f"{table_id}-table-btn", "href"),
            [
                Input("activity-status-filter",   "value"),
                Input("tc-filter",                "value"),
                Input("language-filter",          "value"),
                Input("classification-filter",    "value"),
                Input("app-id-filter",            "value"),
                Input("host-name-filter",         "value"),
            ],
        )
        def update_table_button_href(activity, tc, lang, classification, app_id, host, table_id=table_id):
            qs = {}
            if activity:       qs["activity_status"] = activity
            if tc:             qs["transaction_cycle"] = tc
            if lang:           qs["main_language"] = lang
            if classification: qs["classification_label"] = classification
            if app_id:         qs["app_id"] = app_id
            if host:           qs["host_name"] = host

            base = f"/table-{table_id}"
            return base + "?" + urllib.parse.urlencode(qs) if qs else base