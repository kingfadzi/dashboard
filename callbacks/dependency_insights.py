from dash import Input, Output, State
from dash.exceptions import PreventUpdate

from data.dependencies_fetchers import fetch_no_deps_heatmap_data
from data.dependency_insights import (
    fetch_middleware_usage_detailed, fetch_middleware_usage_by_sub_category, fetch_with_deps_by_variant,
    fetch_avg_deps_per_package_type,
)
from utils.filter_utils import extract_filter_dict_from_store
from viz.viz_dependencies import render_middleware_subcategory_chart
from viz.viz_dependency_insights import render_no_deps_heatmap, render_with_deps_by_variant, \
    render_avg_deps_per_package_type_chart


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

    @app.callback(Output("no-deps-heatmap", "figure"), Input("default-filter-store", "data"))
    def update_no_deps_heatmap(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_no_deps_heatmap(fetch_no_deps_heatmap_data(filters))


    @app.callback(Output("with-deps-by-variant-heatmap", "figure"), Input("default-filter-store", "data"))
    def update_with_deps_by_variant(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_with_deps_by_variant(fetch_with_deps_by_variant(filters))

    @app.callback(Output("avg-deps-per-package-type-chart", "figure"), Input("default-filter-store", "data"))
    def update_avg_deps_per_package_type_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_avg_deps_per_package_type_chart(fetch_avg_deps_per_package_type(filters))

