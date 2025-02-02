import requests
from dash import Input, Output, State
from data.fetch_table_data import fetch_table_data
from callbacks.viz_table_data import viz_table_data

# ✅ Mapping UI Filter Names to SQL Column Names
FILTER_TO_SQL_COLUMN = {
    "repo_id": "r.repo_id",
    "language": "crm.main_language",
    "commits": "crm.number_of_commits",
    "contributors": "crm.number_of_contributors",
    "last_commit": "crm.last_commit_date",
    "host_name": "crm.host_name",
    "activity_status": "crm.activity_status",
    "tc": "crm.tc",
    "classification_label": "crm.classification_label",
    "status": "r.status",
    "app_id": "r.app_id",
}

def construct_rescan_query(main_filters, table_filters=None, batch_size=100, offset=0):
    """Constructs a SQL query for re-scanning repositories based on main & table filters."""

    # ✅ Base SQL Query
    sql_query = """
        SELECT r.*
        FROM Repository r
        JOIN CombinedRepoMetrics crm ON crm.repo_id = r.repo_id
        WHERE 1=1
    """

    # ✅ Initialize Query Parameters
    query_params = {}

    # ✅ Apply Main Filters (Sidebar)
    for ui_filter, sql_column in FILTER_TO_SQL_COLUMN.items():
        value = main_filters.get(ui_filter)
        if value:
            sql_query += f" AND {sql_column} = :{ui_filter}"
            query_params[ui_filter] = value

    # ✅ Apply In-Table Filters (User Searches in Table)
    if table_filters:
        sql_query += f" AND {table_filters}"  # ✅ Appends user-applied table filters directly

    # ✅ Add Pagination
    sql_query += " LIMIT :batch_size OFFSET :offset"
    query_params["batch_size"] = batch_size
    query_params["offset"] = offset

    # ✅ Print SQL Query for Debugging
    print("\n[DEBUG] Constructed SQL Query for Re-Scan:")
    print(sql_query)
    print("Query Parameters:", query_params, "\n")

    return sql_query, query_params

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
            State("temp-table", "filter_query"),  # ✅ Captures table filters
        ],
        prevent_initial_call=True,
    )
    def trigger_rescan(n_clicks, selected_hosts, selected_statuses, selected_tcs, selected_languages, selected_classifications, app_id_input, table_filters):
        """Constructs SQL query from main & table filters, prints it to the console, and sends it to Airflow for repo re-scan."""

        # ✅ Format Main Filters (Sidebar)
        main_filters = {
            "host_name": selected_hosts or None,
            "activity_status": selected_statuses or None,
            "tc": selected_tcs or None,
            "main_language": selected_languages or None,
            "classification_label": selected_classifications or None,
            "app_id": [x.strip() for x in app_id_input.split(",")] if isinstance(app_id_input, str) else None,
        }

        # ✅ Construct SQL Query using both Sidebar & Table Filters
        sql_query, params = construct_rescan_query(main_filters, table_filters)

        # ✅ Print SQL Query to Console
        print(f"\n[DEBUG] Constructed SQL Query for Re-Scan:\n{sql_query}\nQuery Parameters: {params}\n")

        # Send Query to Airflow (Can be integrated later)
        airflow_api_url = "http://your-airflow-host/api/trigger_scan"
        response = requests.post(airflow_api_url, json={"query": sql_query})

        if response.status_code == 200:
            return "Re-Scan request sent successfully!"
        else:
            return f"Failed to send Re-Scan request. Error: {response.text}"