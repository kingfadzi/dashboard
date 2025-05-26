import math
from dash import Input, Output
from data.fetch_table_data import fetch_table_data
from viz.viz_table_data import viz_table_data

def register_table_callbacks(app):
    @app.callback(
        [
            Output("temp-table", "data"),
            Output("temp-table", "tooltip_data"),
            Output("temp-table", "page_count"),
        ],
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
            Input("temp-table", "page_current"),
            Input("temp-table", "page_size"),
        ],
    )
    def update_table(
            host_names,
            statuses,
            tcs,
            languages,
            classifications,
            app_id_input,
            page_current,
            page_size,
    ):
        filters = {
            "host_name": host_names or [],
            "activity_status": statuses or [],
            "transaction_cycle": tcs or [],
            "main_language": languages or [],
            "classification_label": classifications or [],
            "app_id": app_id_input.strip() if app_id_input else None,
        }

        df, total_count = fetch_table_data(filters, page_current, page_size)
        table_data = viz_table_data(df)

        tooltip_data = []
        for row in table_data:
            row_tooltip = {}
            for key, value in row.items():
                if key in ["transaction_cycle", "app_id"]:
                    row_tooltip[key] = {"value": str(value), "type": "text"}
                else:
                    row_tooltip[key] = {"value": "", "type": "text"}
            tooltip_data.append(row_tooltip)

        return table_data, tooltip_data, math.ceil(total_count / page_size)
