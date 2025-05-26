import pandas as pd
from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate
from sqlalchemy import text
from data.cache_instance import cache
from data.db_connection import engine
from data.sql_filter_utils import build_repo_filter_conditions


@callback(
    Output("code-insights-modal", "is_open"),
    [Input("code-insights-modal-open", "n_clicks"),
     Input("code-insights-modal-close", "n_clicks")],
    State("code-insights-modal", "is_open"),
)
def toggle_modal(n_open, n_close, is_open):
    if n_open or n_close:
        return not is_open
    raise PreventUpdate


@callback(
    Output("code-insights-table", "data"),
    Output("code-insights-table", "columns"),
    Output("code-insights-total", "children"),
    Output("code-insights-total", "is_open"),
    Input("code-insights-table", "page_current"),
    Input("code-insights-table", "page_size"),
    Input("code-insights-table", "sort_by"),
    Input("code-insights-modal", "is_open"),
    State("default-filter-store", "data"),
)
def load_table_data(page_current, page_size, sort_by, is_open, filters):
    if not is_open:
        raise PreventUpdate

    # Generate WHERE clause and parameters from filters
    condition_string, param_dict = build_repo_filter_conditions(filters)
    extra_where = f" AND {condition_string}" if condition_string else ""

    # Sorting logic
    if sort_by:
        sort_col = sort_by[0]["column_id"]
        sort_dir = sort_by[0]["direction"].upper()
        order_clause = f"ORDER BY {sort_col} {sort_dir}"
    else:
        order_clause = "ORDER BY hr.repo_id DESC"

    # Pagination parameters
    param_dict["limit"] = page_size
    param_dict["offset"] = page_current * page_size

    # Main query
    base_sql = """
        SELECT hr.repo_id, hr.repo_slug, hr.app_id, hr.classification_label,
               hr.main_language, hr.all_languages, hr.activity_status
        FROM harvested_repositories hr
        LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id
        WHERE TRUE {extra_where}
        {order_clause}
        LIMIT :limit OFFSET :offset
    """
    stmt = text(base_sql.format(extra_where=extra_where, order_clause=order_clause))
    df = pd.read_sql(stmt, engine, params=param_dict)

    # Total count query
    count_sql = f"""
        SELECT COUNT(*) AS total
        FROM harvested_repositories hr
        LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id
        WHERE TRUE {extra_where}
    """
    total = pd.read_sql(text(count_sql), engine, params=param_dict).iloc[0]["total"]

    # Format columns and return
    columns = [{"name": col, "id": col} for col in df.columns]
    return df.to_dict("records"), columns, f"{total:,} repositories matched.", True
