import re
from dash import Input, Output, State
from data.fetch_table_data import fetch_table_data
from viz.viz_table_data import viz_table_data

def register_table_callbacks(app):
    @app.callback(
        [
            Output("temp-table", "data"),
            Output("temp-table", "tooltip_data"),
        ],
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
            Input("temp-table", "page_current"),  # Pagination
            Input("temp-table", "page_size"),     # Pagination
        ],
    )
    def update_table(*args):
        filter_keys = ["host_name", "activity_status", "tc", "main_language", "classification_label", "app_id"]
        filters = {key: (arg if arg else []) for key, arg in zip(filter_keys, args[:-2])}

        page_current = args[-2]
        page_size = args[-1]

        print("\nFilters Passed to `fetch_table_data()`:")
        print(filters, f"Page Current: {page_current}, Page Size: {page_size}\n")

        # Fetch paginated data
        table_raw_df = fetch_table_data(filters, page_current=page_current, page_size=page_size)
        table_data = viz_table_data(table_raw_df)

        # Generate tooltip_data for TC and App ID fields
        tooltip_data = []
        for row in table_data:
            row_tooltip = {}
            for key, value in row.items():
                if key in ["tc", "app_id"]:
                    row_tooltip[key] = {"value": str(value), "type": "text"}
                else:
                    row_tooltip[key] = {"value": "", "type": "text"}
            tooltip_data.append(row_tooltip)

        return table_data, tooltip_data
