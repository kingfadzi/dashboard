from dash import Output, Input
from data.code_insights_lizard_fetchers import (
    fetch_total_ccn_buckets,
    fetch_function_count_buckets,
    fetch_total_nloc_buckets,
    fetch_ccn_vs_function_count,
)
from viz.viz_code_insights_lizard import (
    render_total_ccn_chart,
    render_function_count_chart,
    render_total_nloc_chart,
    render_ccn_vs_function_count_chart,
)
from utils.filter_utils import extract_filter_dict_from_store

def register_code_insights_lizard_callbacks(app):

    @app.callback(Output("total-ccn-chart", "figure"), Input("default-filter-store", "data"))
    def update_total_ccn_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_total_ccn_buckets(filters)
        return render_total_ccn_chart(df)

    @app.callback(Output("function-count-chart", "figure"), Input("default-filter-store", "data"))
    def update_function_count_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_function_count_buckets(filters)
        return render_function_count_chart(df)

    @app.callback(Output("total-nloc-chart", "figure"), Input("default-filter-store", "data"))
    def update_total_nloc_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_total_nloc_buckets(filters)
        return render_total_nloc_chart(df)

    @app.callback(Output("ccn-vs-function-count-chart", "figure"), Input("default-filter-store", "data"))
    def update_ccn_vs_function_count_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_ccn_vs_function_count(filters)
        return render_ccn_vs_function_count_chart(df)
