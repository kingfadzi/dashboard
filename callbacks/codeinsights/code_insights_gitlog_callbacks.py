from dash import Input, Output
from data.codeinsights.code_insights_gitlog_fetchers import (
    fetch_avg_file_size_buckets,
    fetch_contributor_dominance,
    fetch_branch_sprawl,
    fetch_repo_age_buckets
)
from viz.codeinsights.viz_code_insights_gitlog import (
    render_avg_file_size_chart,
    render_contributor_dominance_chart,
    render_branch_sprawl_chart,
    render_repo_age_chart
)
from utils.filter_utils import extract_filter_dict_from_store

def register_code_insights_gitlog_callbacks(app):

    @app.callback(Output("avg-file-size-chart", "figure"), Input("default-filter-store", "data"))
    def update_avg_file_size_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_avg_file_size_buckets(filters)
        fig = render_avg_file_size_chart(df)
        return fig

    @app.callback(Output("contributor-dominance-chart", "figure"), Input("default-filter-store", "data"))
    def update_contributor_dominance_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_contributor_dominance(filters)
        fig = render_contributor_dominance_chart(df)
        return fig


    @app.callback(Output("branch-sprawl-chart", "figure"), Input("default-filter-store", "data"))
    def update_branch_sprawl_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_branch_sprawl(filters)
        fig = render_branch_sprawl_chart(df)
        return fig


    @app.callback(Output("repo-age-chart", "figure"), Input("default-filter-store", "data"))
    def update_repo_age_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_repo_age_buckets(filters)
        fig = render_repo_age_chart(df)
        return fig

