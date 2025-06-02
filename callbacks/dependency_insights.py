from dash import Input, Output
from data.dependency_insights import (
    fetch_outdated_library_usage,
    fetch_legacy_version_usage,
    fetch_junit_version_usage,
    fetch_dependency_count_per_repo,
    fetch_frameworks_per_repo,
)
from viz.viz_dependency_insights import (
    render_outdated_library_chart,
    render_legacy_version_chart,
    render_junit_version_chart,
    render_dependency_count_chart,
    render_frameworks_per_repo_chart,
)

def register_dependency_insights_callbacks(app):
    @app.callback(
        Output("outdated-library-chart", "figure"),
        Input("default-filter-store", "data"),
    )
    def update_outdated_library_chart(store_data):
        df = fetch_outdated_library_usage(store_data)
        return render_outdated_library_chart(df)

    @app.callback(
        Output("legacy-version-chart", "figure"),
        Input("default-filter-store", "data"),
    )
    def update_legacy_version_chart(store_data):
        df = fetch_legacy_version_usage(store_data)
        return render_legacy_version_chart(df)

    @app.callback(
        Output("junit-version-chart", "figure"),
        Input("default-filter-store", "data"),
    )
    def update_junit_version_chart(store_data):
        df = fetch_junit_version_usage(store_data)
        return render_junit_version_chart(df)

    @app.callback(
        Output("dependency-count-chart", "figure"),
        Input("default-filter-store", "data"),
    )
    def update_dependency_count_chart(store_data):
        df = fetch_dependency_count_per_repo(store_data)
        return render_dependency_count_chart(df)

    @app.callback(
        Output("frameworks-per-repo-chart", "figure"),
        Input("default-filter-store", "data"),
    )
    def update_frameworks_per_repo_chart(store_data):
        df = fetch_frameworks_per_repo(store_data)
        return render_frameworks_per_repo_chart(df)