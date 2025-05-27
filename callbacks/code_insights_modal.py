# callbacks/code_insights_callbacks.py
import pandas as pd
from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate
from sqlalchemy import text
from data.db_connection import engine
from data.sql_filter_utils import build_repo_filter_conditions

@callback(
    Output("default-filter-store", "data"),
    Input("main_language-filter", "value"),
    Input("activity-status-filter", "value"),
    Input("tc-filter", "value"),  # transaction_cycle
    Input("classification-filter", "value"),  # classification_label
    Input("app-id-filter", "value"),
    Input("host-name-filter", "value"),
)
def update_filter_store(main_lang, status, tc, classification, app_id, host_name):
    filters = {}
    if main_lang:
        filters["main_language"] = main_lang
    if status:
        filters["activity_status"] = status
    if tc:
        filters["transaction_cycle"] = tc
    if classification:
        filters["classification_label"] = classification
    if app_id:
        filters["app_id"] = app_id
    if host_name:
        filters["host_name"] = host_name

    print("Updated filter store:", filters)
    return filters

@callback(
    Output("filters-applied-trigger", "data"),
    Input("default-filter-store", "data"),
)
def sync_filters_applied_trigger(filters):
    print("Filter store updated:", filters)
    if not filters:
        raise PreventUpdate
    return {"updated": True}

@callback(
    Output("code-insights-modal", "is_open"),
    [Input("code-insights-modal-open", "n_clicks"),
     Input("code-insights-modal-close", "n_clicks")],
    State("code-insights-modal", "is_open"),
)
def toggle_modal(n_open, n_close, is_open):
    if n_open or n_close:
        print("Toggling modal:", not is_open)
        return not is_open
    raise PreventUpdate

@callback(
    Output("code-insights-table", "data"),
    Output("code-insights-table", "columns"),
    Output("code-insights-total", "children"),
    Output("code-insights-total", "is_open"),
    Input("code-insights-modal", "is_open"),
    Input("filters-applied-trigger", "data"),
    State("default-filter-store", "data"),
    State("code-insights-table", "page_current"),
    State("code-insights-table", "page_size"),
    State("code-insights-table", "sort_by"),
)
def load_table_data(is_open, _, filters, page_current, page_size, sort_by):
    print("Modal open:", is_open)
    print("Current filters:", filters)

    if not is_open or not filters or not isinstance(filters, dict) or not filters.keys():
        print("Preventing update due to missing or empty filters.")
        raise PreventUpdate

    condition_string, param_dict = build_repo_filter_conditions(filters)
    print("Condition string:", condition_string)
    print("SQL params:", param_dict)

    extra_where = f" AND {condition_string}" if condition_string else ""

    order_clause = (
        f"ORDER BY {sort_by[0]['column_id']} {sort_by[0]['direction'].upper()}"
        if sort_by else "ORDER BY hr.repo_id DESC"
    )

    param_dict["limit"] = page_size
    param_dict["offset"] = page_current * page_size

    stmt = text(f"""
        SELECT hr.repo_id, hr.repo_slug, hr.app_id, hr.classification_label,
               hr.main_language, hr.all_languages, hr.activity_status
        FROM harvested_repositories hr
        LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id
        WHERE TRUE {extra_where}
        {order_clause}
        LIMIT :limit OFFSET :offset
    """)
    df = pd.read_sql(stmt, engine, params=param_dict)

    count_stmt = text(f"""
        SELECT COUNT(*) AS total
        FROM harvested_repositories hr
        LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id
        WHERE TRUE {extra_where}
    """)
    total = pd.read_sql(count_stmt, engine, params=param_dict).iloc[0]["total"]

    columns = [{"name": col, "id": col} for col in df.columns]
    return df.to_dict("records"), columns, f"{total:,} repositories matched.", True
