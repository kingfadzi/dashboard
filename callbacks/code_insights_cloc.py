from dash import Input, Output
from data.code_insights_cloc_fetchers import (
    fetch_code_volume_by_language,
    fetch_file_count_by_language,
    fetch_code_composition_by_language,
    fetch_code_file_scatter,
)
from viz.viz_code_insights_cloc import (
    render_code_volume_chart,
    render_file_count_chart,
    render_code_composition_chart,
    render_code_file_scatter_chart,
)
from utils.filter_utils import extract_filter_dict_from_store

def register_code_insights_cloc_callbacks(app):
    @app.callback(Output("code-volume-chart", "figure"), Input("default-filter-store", "data"))
    def update_code_volume_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_code_volume_by_language(filters)
        return render_code_volume_chart(df).figure

    @app.callback(Output("file-count-chart", "figure"), Input("default-filter_store", "data"))
    def update_file_count_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_file_count_by_language(filters)
        return render_file_count_chart(df).figure

    @app.callback(Output("code-composition-chart", "figure"), Input("default-filter-store", "data"))
    def update_code_composition_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_code_composition_by_language(filters)
        return render_code_composition_chart(df).figure

    @app.callback(Output("code-file-scatter-chart", "figure"), Input("default-filter-store", "data"))
    def update_code_file_scatter_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_code_file_scatter(filters)
        return render_code_file_scatter_chart(df).figure
