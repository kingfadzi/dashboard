from dash import Input, Output
from data.build_info_fetchers import (
    fetch_detection_coverage_by_tool,
    fetch_module_counts_per_repo,
    fetch_runtime_versions_by_tool,
    fetch_status_by_tool,
    fetch_runtime_fragmentation_by_tool,
    fetch_confidence_distribution,
)
from viz.viz_build_info import (
    render_detection_coverage_chart,
    render_module_count_chart,
    render_runtime_versions_chart,
    render_status_by_tool_chart,
    render_runtime_fragmentation_chart,
    render_confidence_distribution_chart,
)

TOP_RUNTIMES = 20

def register_build_info_callbacks(app):
    filter_inputs = [
        Input("host-name-filter", "value"),
        Input("app-id-filter", "value"),
        Input("tc-filter", "value"),
        Input("language-filter", "value"),
        Input("classification-filter", "value"),
        Input("activity-status-filter", "value"),
    ]

    filter_keys = ["host_name", "app_id", "transaction_cycle", "main_language", "classification_label", "activity_status"]

    @app.callback(Output("detection-coverage-chart", "figure"), filter_inputs)
    def update_detection_chart(*vals):
        filters = dict(zip(filter_keys, vals))
        df = fetch_detection_coverage_by_tool(filters)
        return render_detection_coverage_chart(df)

    @app.callback(Output("module-count-chart", "figure"), filter_inputs)
    def update_module_chart(*vals):
        filters = dict(zip(filter_keys, vals))
        df = fetch_module_counts_per_repo(filters)
        return render_module_count_chart(df)

    @app.callback(Output("status-by-tool-chart", "figure"), filter_inputs)
    def update_status_chart(*vals):
        filters = dict(zip(filter_keys, vals))
        df = fetch_status_by_tool(filters)
        return render_status_by_tool_chart(df)

    @app.callback(Output("runtime-fragmentation-chart", "figure"), filter_inputs)
    def update_runtime_fragmentation_chart(*vals):
        filters = dict(zip(filter_keys, vals))
        df = fetch_runtime_fragmentation_by_tool(filters)
        return render_runtime_fragmentation_chart(df)

    @app.callback(Output("confidence-distribution-chart", "figure"), filter_inputs)
    def update_confidence_chart(*vals):
        filters = dict(zip(filter_keys, vals))
        df = fetch_confidence_distribution(filters)
        return render_confidence_distribution_chart(df)

    @app.callback(
        Output("runtime-versions-chart", "figure"),
        Output("tool-selector", "options"),
        Input("tool-selector", "value"),
        *filter_inputs,
    )
    def update_runtime_versions_chart(selected_tool, *vals):
        filters = dict(zip(filter_keys, vals))
        df = fetch_runtime_versions_by_tool(filters)
        all_tools = sorted(df["tool"].dropna().unique())
        options = [{"label": t, "value": t} for t in all_tools]

        if selected_tool:
            df = df[df["tool"] == selected_tool]

        df = df.sort_values("repo_count", ascending=False).head(TOP_RUNTIMES)
        return render_runtime_versions_chart(df), options
