from dash import Input, Output, State, callback, no_update
import urllib.parse
from dash.exceptions import PreventUpdate

from data.fetch_table_data import fetch_table_data
from utils.filter_utils import extract_filter_dict_from_store

# Extract page=N from query string
def extract_page_from_search(search):
    if not search:
        return None
    parsed = urllib.parse.parse_qs(search.lstrip("?"))
    try:
        page = int(parsed.get("page", [1])[0])
        return max(page - 1, 0)  # AG Grid expects 0-based
    except Exception:
        return None

# Generate table data and column definitions
def get_table_outputs(store_data, current_path=None, current_search=None):
    filters = extract_filter_dict_from_store(store_data or {})
    df, _ = fetch_table_data(filters, 0, 1000)
    table_data = df.to_dict("records")

    base_path = current_path.split("?")[0] if current_path else "/table-overview"
    current_page = extract_page_from_search(current_search)
    current_page = current_page + 1 if current_page is not None else 1

    return_url_with_page = f"{base_path}?page={current_page}"
    encoded_return_url = urllib.parse.quote(return_url_with_page)

    column_defs = [
        {
            "headerName": "Repo Name",
            "field": "repo_id",
            "cellRenderer": "markdown",
            "valueGetter": {
                "function": f"`[${'{'}params.data.repo_id{'}'}](/repo?repo_id=${'{'}params.data.repo_id{'}'}&returnUrl={encoded_return_url})`"
            },
            "filterValueGetter": {"function": "params.data.repo_id"},
            "cellRendererParams": {
                "linkTarget": "_self",
                "html": True
            }
        },
        {
            "headerName": "App ID",
            "field": "app_id",
            "cellRenderer": "markdown",
            "valueGetter": {
                "function": f"`[${'{'}params.data.app_id{'}'}](${ '{' }params.data.browse_url{'}'})`"
            },
            "filterValueGetter": {"function": "params.data.app_id"},
            "cellRendererParams": {
                "linkTarget": "_blank",
                "html": True
            }
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
            }
        },
    ]

    return table_data, column_defs

def register_table_callbacks(app):
    for table_id in ["overview", "build-info", "code-insights", "dependencies"]:
        @app.callback(
            Output(f"{table_id}-table", "rowData"),
            Output(f"{table_id}-table", "columnDefs"),
            Output(f"{table_id}-table", "paginationGoTo"),
            Input("default-filter-store", "data"),
            State("url", "pathname"),
            State("url", "search"),
        )
        def update_table(store_data, current_path, search):
            table_data, column_defs = get_table_outputs(store_data, current_path, search)
            page = extract_page_from_search(search)
            return table_data, column_defs, page if page is not None else no_update

        # Store current pagination page to URL
        @app.callback(
            Output("url", "search", allow_duplicate=True),
            Input(f"{table_id}-table", "eventData"),
            State("url", "pathname"),
            prevent_initial_call=True,
        )
        def update_url_on_page_change(event, pathname):
            if not event or "currentPage" not in event:
                raise PreventUpdate
            new_page = int(event["currentPage"]) + 1  # Make it 1-based
            return f"?page={new_page}"

    # Filter store update
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
