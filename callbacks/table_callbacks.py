# callbacks/table_callbacks.py

import requests
import re
from dash import Input, Output, State
from data.fetch_table_data import fetch_table_data
from callbacks.viz_table_data import viz_table_data

AIRFLOW_URL = "http://192.168.1.188:8088/api/v1/dags/fundamental_metrics/dagRuns"
AIRFLOW_AUTH = ("admin", "password")

def prepare_filter_payload(filters, table_filters=None):

    print("\n[DEBUG] Sidebar Filters Before Processing:", filters, "\n")

    payload = {}

    for key, value in filters.items():
        if value:
            payload[key] = value if isinstance(value, list) else [value]

    if table_filters:
        print("\nTable Filters Received:", table_filters, "\n")

        for condition in table_filters.split(" && "):
            match = re.match(r"\{(.+?)\} (icontains|contains|>|<|>=|<=|=) \"?(.+?)\"?$", condition)
            if match:
                column_name, _, value = match.groups()

                if column_name in payload:
                    print(f"Overwriting {column_name}: {payload[column_name]} -> [{value}]")
                payload[column_name] = [value]

    print("\nFinal Payload Sent to Airflow:", payload, "\n")

    return payload

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
        filter_keys = ["host_name", "activity_status", "tc", "main_language", "classification_label", "app_id"]
        filters = {key: (arg if arg else []) for key, arg in zip(filter_keys, args)}

        print("\nFilters Passed to `fetch_table_data()`:")
        print(filters, "\n")

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
        main_filters = {
            "host_name": selected_hosts or [],
            "activity_status": selected_statuses or [],
            "tc": selected_tcs or [],
            "main_language": selected_languages or [],
            "classification_label": selected_classifications or [],
            "app_id": [x.strip() for x in app_id_input.split(",")] if isinstance(app_id_input, str) else [],
        }

        print("\nSidebar Filters Before Payload Processing:")
        print(main_filters, "\n")

        payload = prepare_filter_payload(main_filters, table_filters)

        try:
            response = requests.post(AIRFLOW_URL, json={"conf": payload}, auth=AIRFLOW_AUTH)

            if response.status_code == 200:
                return "Re-Scan request sent successfully to Airflow!"
            else:
                return f"Failed to send Re-Scan request. Error: {response.text}"

        except requests.RequestException as e:
            return f"Error connecting to Airflow: {str(e)}"
