from dash import Input, Output
from data.fetch_markup_language import fetch_markup_language_usage
from data.code_insights_enry_fetchers import fetch_role_distribution, fetch_language_bubble_chart_data
from callbacks.redirect_callbacks import generate_redirect_callbacks
from utils.filter_utils import extract_filter_dict_from_store
from viz.viz_code_insights_charts import render_role_distribution_chart, render_language_mixed_chart
from viz.viz_code_insights_markup import render_markup_language_usage_chart

def register_code_insights_callbacks(app):

    @app.callback(
        Output("role-distribution-chart", "figure"),
        Input("default-filter-store", "data")
    )
    def update_role_distribution(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_role_distribution(filters)
        fig = render_role_distribution_chart(df)
        return fig


    @app.callback(
        Output("language-bubble-chart", "figure"),
        Input("default-filter-store", "data")
    )
    def update_language_bubble_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_language_mixed_chart(fetch_language_bubble_chart_data(filters)).figure

    @app.callback(Output("markup-language-usage-chart", "figure"), Input("default-filter-store", "data"))
    def update_markup_usage(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_markup_language_usage_chart(fetch_markup_language_usage(filters))

    generate_redirect_callbacks(
        app,
        target_href="/table-code-insights",
        button_id="code-insights-table-btn",
        output_container_id="code-insights-table-link-container",
        reverse_href="/code-insights",
        reverse_button_id="back-to-charts-btn-code-insights",
    )
