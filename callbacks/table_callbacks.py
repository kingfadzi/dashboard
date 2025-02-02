# callbacks/table_callbacks.py

import requests
import re
from dash import Input, Output, State
from data.fetch_table_data import fetch_table_data
from callbacks.viz_table_data import viz_table_data

FILTER_TO_SQL_COLUMN = {
    "repo_id": "repo_id",
    "web_url": "web_url",
    "language": "main_language",
    "commits": "total_commits",
    "contributors": "number_of_contributors",
    "last_commit": "last_commit_date",
    "host_name": "crm.host_name",
    "activity_status": "crm.activity_status",
    "tc": "crm.tc",
    "classification_label": "crm.classification_label",
    "status": "r.status",
    "app_id": "r.app_id",
}

def construct_rescan_query(filters, table_filters=None):
    """Constructs a SQL query for re-scanning repositories based on applied filters."""

    sql_query = """
        SELECT repo_id, web_url, main_language AS language, total_commits AS commits,
               number_of_contributors AS contributors, last_commit_date AS last_commit
        FROM combined_repo_metrics
        WHERE 1=1
    """

    query_params = {}

    for ui_filter, sql_column in FILTER_TO_SQL_COLUMN.items():
        value = filters.get(ui_filter)

        if value:
            if isinstance(value, list) and len(value) > 1:
                placeholders = ", ".join([f"'{v}'" for v in value])
                sql_query += f" AND {sql_column} IN ({placeholders})"
            else:
                sql_query += f" AND {sql_column} = '{value[0]}'" if isinstance(value, list) else f" AND {sql_column} = '{value}'"
                query_params[ui_filter] = value

    table_filter_sql = parse_table_filters(table_filters)
    if table_filter_sql:
        sql_query += f" AND {table_filter_sql}"

    print("\n[DEBUG] Constructed SQL Query for Re-Scan (Sent to Airflow):")
    print(sql_query)
    print("Query Parameters:", query_params, "\n")

    return sql_query, query_params

def parse_table_filters(filter_query):
    """Parses Dash DataTable filter_query and maps to SQL column names."""
    if not filter_query:
        return ""

    sql_conditions = []
    conditions = filter_query.split(" && ")

    for condition in conditions:
        match = re.match(r"\{(.+?)\} (contains|>|<|>=|<=|=) \"?(.+?)\"?$", condition)
        if match:
            column_name, operator, value = match.groups()
            sql_column = FILTER_TO_SQL_COLUMN.get(column_name)

            if sql_column:
                if operator == "contains":
                    sql_conditions.append(f"{sql_column} LIKE '%{value}%'")
                else:
                    sql_conditions.append(f"{sql_column} {operator} '{value}'")

    return " AND ".join(sql_conditions)

def register_table_callbacks(app):
    @app.callback(
        Output("temp-table", "data"),
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
        ],
    )
    def update_table(*args):
        """Fetches table data using `fetch_table_data()` with correct filters."""
        filter_keys = ["host_name", "activity_status", "tc", "main_language", "classification_label", "app_id"]
        filters = {key: (arg if arg else None) for key, arg in zip(filter_keys, args)}

        table_raw_df = fetch_table_data(filters)
        return viz_table_data(table_raw_df)

    @app.callback(
        Output("rescan-status", "children"),
        Input("rescan-button", "n_clicks"),
        [
            State("host-name-filter", "value"),
            State("activity-status-filter", "value"),
            State("tc-filter", "value"),
            State("language-filter", "value"),
            State("classification-filter", "value"),
            State("app-id-filter", "value"),
            State("temp-table", "filter_query"),
        ],
        prevent_initial_call=True,
    )
    def trigger_rescan(n_clicks, selected_hosts, selected_statuses, selected_tcs, selected_languages, selected_classifications, app_id_input, table_filters):
        """Constructs SQL query from main & table filters, prints it, and sends it to Airflow for repo re-scan."""

        main_filters = {
            "host_name": selected_hosts or None,
            "activity_status": selected_statuses or None,
            "tc": selected_tcs or None,
            "main_language": selected_languages or None,
            "classification_label": selected_classifications or None,
            "app_id": [x.strip() for x in app_id_input.split(",")] if isinstance(app_id_input, str) else None,
        }

        sql_query, params = construct_rescan_query(main_filters, table_filters)

        print(f"\n[DEBUG] Final SQL Query Sent to Airflow:\n{sql_query}\nQuery Parameters: {params}\n")

        return "Re-Scan request sent successfully to Airflow!"