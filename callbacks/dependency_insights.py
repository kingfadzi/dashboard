from dash import Input, Output, State
from dash.exceptions import PreventUpdate


from data.dependency_insights import (
    fetch_middleware_usage_detailed, fetch_middleware_usage_by_sub_category,
)
from utils.filter_utils import extract_filter_dict_from_store
from viz.viz_dependencies import render_middleware_subcategory_chart

def register_dependency_insights_callbacks(app):
    @app.callback(
        Output("middleware-subcategory-dropdown", "options"),
        Input("middleware-subcategory-dropdown", "id")  # dummy input
    )
    def populate_subcategory_dropdown(_):
        df = fetch_middleware_usage_detailed()
        options = sorted(df["sub_category"].dropna().unique())
        return [{"label": s, "value": s} for s in options]

    @app.callback(
        Output("middleware-subcategory-chart", "figure"),
        Input("middleware-subcategory-dropdown", "value"),
        State("default-filter-store", "data"),
    )
    def update_middleware_chart(selected_subcategory, filters):
        filters = filters or {}  # ← Ensure it's a dict
        df = fetch_middleware_usage_by_sub_category(filters)

        print("Selected subcategory:", selected_subcategory)
        print("Filters:", filters)
        print("Middleware Data:")
        print(df.head())

        if selected_subcategory:
            df = df[df["sub_category"] == selected_subcategory]

        if df.empty:
            raise PreventUpdate

        return render_middleware_subcategory_chart(df)




