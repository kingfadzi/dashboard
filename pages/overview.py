import dash
from dash import html, Input, Output, State, callback
from layouts.layout_charts import chart_layout
from components.overview_table import render_overview_table
from data.fetch_table_data import fetch_table_data

# Register this as the default ("Overview") page
dash.register_page(__name__, path="/")

# Page layout container
layout = html.Div(id="overview-content")


# === Graph View Callback ===
@callback(
    Output("overview-content", "children"),
    Input("view-mode", "data"),
    Input("host-name-filter", "value"),
    Input("activity-status-filter", "value"),
    Input("tc-filter", "value"),
    Input("language-filter", "value"),
    Input("classification-filter", "value"),
    Input("app-id-filter", "value"),
)
def render_graph_view(view_mode, host_names, statuses, tcs, languages, classifications, app_id_input):
    if view_mode != "graph":
        raise dash.exceptions.PreventUpdate

    filters = {
        "host_name": host_names or [],
        "activity_status": statuses or [],
        "tc": tcs or [],
        "main_language": languages or [],
        "classification_label": classifications or [],
        "app_id": app_id_input.strip() if app_id_input else None,
    }

    return chart_layout(filters)


