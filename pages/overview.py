import dash
from dash import html, Input, Output, State, callback
from layouts.layout_charts import chart_layout
from layouts.layout_table import table_layout
from data.fetch_table_data import fetch_table_data
from viz.overview_table import viz_table_data

dash.register_page(__name__, path="/")

layout = html.Div(id="overview-content")

@callback(
    Output("overview-content", "children"),
    Input("view-mode", "data"),
    Input("overview-table", "page_current"),
    Input("overview-table", "page_size"),
    State("host-name-filter", "value"),
    State("activity-status-filter", "value"),
    State("tc-filter", "value"),
    State("language-filter", "value"),
    State("classification-filter", "value"),
    State("app-id-filter", "value"),
)
def render_overview(view_mode, page_current, page_size,
                    host_names, statuses, tcs, languages, classifications, app_id_input):
    filters = {
        "host_name": host_names or [],
        "activity_status": statuses or [],
        "tc": tcs or [],
        "main_language": languages or [],
        "classification_label": classifications or [],
        "app_id": app_id_input.strip() if app_id_input else None,
    }

    if view_mode == "graph":
        return chart_layout(filters)

    current = page_current or 0
    size = page_size or 10
    df, total_count = fetch_table_data(filters=filters, page_current=current, page_size=size)
    return table_layout(viz_table_data(df), total_count, current, size)