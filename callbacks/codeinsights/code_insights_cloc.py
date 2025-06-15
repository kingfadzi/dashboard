from dash import Input, Output
from data.codeinsights.code_insights_cloc_fetchers import (
    fetch_code_composition_by_language,
    fetch_code_file_scatter,
)
from viz.codeinsights.viz_code_insights_cloc import (

    render_code_composition_chart,
    render_code_file_scatter_chart,
)
from utils.filter_utils import extract_filter_dict_from_store

def register_code_insights_cloc_callbacks(app):

    @app.callback(Output("code-composition-chart", "figure"), Input("default-filter-store", "data"))
    def update_code_composition_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_code_composition_by_language(filters)
        fig = render_code_composition_chart(df)
        return fig


    @app.callback(Output("code-file-scatter-chart", "figure"), Input("default-filter-store", "data"))
    def update_code_file_scatter_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_code_file_scatter(filters)
        return render_code_file_scatter_chart(df)

