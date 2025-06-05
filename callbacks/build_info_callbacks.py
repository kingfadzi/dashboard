from dash import Input, Output

from data.build_info_fetchers import (
    fetch_detection_coverage_by_tool,
    fetch_module_counts_per_repo,
    fetch_runtime_versions_by_tool,
    fetch_status_by_tool,
    fetch_runtime_fragmentation_by_tool,
    fetch_confidence_distribution, fetch_runtime_build_coverage_by_language, fetch_build_tool_variants,
    fetch_no_buildtool_language_type_distribution, fetch_dotnet_support_status_summary,
    fetch_java_support_status_summary, fetch_python_support_status_summary, fetch_js_support_status_summary,
    fetch_go_support_status_summary,
)
from callbacks.redirect_callbacks import generate_redirect_callbacks
from viz.viz_build_info import (
    render_detection_coverage_chart,
    render_module_count_chart,
    render_runtime_versions_chart,
    render_status_by_tool_chart,
    render_runtime_fragmentation_chart,
    render_confidence_distribution_chart, render_runtime_build_heatmap, render_build_tool_variant_chart,
    render_no_buildtool_language_type_distribution, render_dotnet_support_status_chart,
    render_java_support_status_chart, render_python_support_status_chart, render_js_support_status_chart,
    render_go_support_status_chart,
)
from utils.filter_utils import extract_filter_dict_from_store
from dash import Output, Input
from data.build_info_fetchers import fetch_no_buildtool_repo_scatter
from viz.viz_build_info import render_no_buildtool_scatter


TOP_RUNTIMES = 20

def register_build_info_callbacks(app):
    @app.callback(Output("detection-coverage-chart", "figure"), Input("default-filter-store", "data"))
    def update_detection_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_detection_coverage_by_tool(filters)
        return render_detection_coverage_chart(df)

    @app.callback(Output("module-count-chart", "figure"), Input("default-filter-store", "data"))
    def update_module_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_module_counts_per_repo(filters)
        return render_module_count_chart(df)

    @app.callback(Output("status-by-tool-chart", "figure"), Input("default-filter-store", "data"))
    def update_status_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_status_by_tool(filters)
        return render_status_by_tool_chart(df)

    @app.callback(Output("runtime-fragmentation-chart", "figure"), Input("default-filter-store", "data"))
    def update_runtime_fragmentation_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_runtime_fragmentation_by_tool(filters)
        return render_runtime_fragmentation_chart(df)

    @app.callback(Output("confidence-distribution-chart", "figure"), Input("default-filter-store", "data"))
    def update_confidence_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_confidence_distribution(filters)
        return render_confidence_distribution_chart(df)

    @app.callback(
        Output("runtime-versions-chart", "figure"),
        Output("tool-selector", "options"),
        Input("tool-selector", "value"),
        Input("default-filter-store", "data"),
    )
    def update_runtime_versions_chart(selected_tool, store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_runtime_versions_by_tool(filters)
        all_tools = sorted(df["tool"].dropna().unique())
        options = [{"label": t, "value": t} for t in all_tools]

        if selected_tool:
            df = df[df["tool"] == selected_tool]

        df = df.sort_values("repo_count", ascending=False).head(TOP_RUNTIMES)
        return render_runtime_versions_chart(df), options

    @app.callback(Output("build-runtime-coverage-chart", "figure"), Input("default-filter-store", "data"))
    def update_runtime_coverage_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_runtime_build_coverage_by_language(filters)
        return render_runtime_build_heatmap(df)

    @app.callback(Output("build-tool-variant-chart", "figure"), Input("default-filter-store", "data"))
    def update_build_tool_variant_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_build_tool_variants(filters)
        return render_build_tool_variant_chart(df)
        
    

    @app.callback(
        Output("no-buildtool-scatter", "figure"),
        Input("default-filter-store", "data")
    )
    def update_no_buildtool_scatter(filters):
        df = fetch_no_buildtool_repo_scatter(filters)
        return render_no_buildtool_scatter(df)


    @app.callback(
        Output("no-buildtool-language-distribution", "figure"),
        Input("default-filter-store", "data")
    )
    def update_no_buildtool_language_distribution(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_no_buildtool_language_type_distribution(filters)
        return render_no_buildtool_language_type_distribution(df)

    @app.callback(
        Output("dotnet-support-status-chart", "figure"),
        Input("default-filter-store", "data")
    )
    def update_dotnet_support_status_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_dotnet_support_status_summary(filters)
        return render_dotnet_support_status_chart(df)

    @app.callback(
        Output("java-support-status-chart", "figure"),
        Input("default-filter-store", "data")
    )
    def update_java_support_status_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_java_support_status_summary(filters)
        return render_java_support_status_chart(df)


    @app.callback(
        Output("python-support-status-chart", "figure"),
        Input("default-filter-store", "data")
    )
    def update_python_support_status_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_python_support_status_summary(filters)
        return render_python_support_status_chart(df)


    @app.callback(
        Output("js-support-status-chart", "figure"),
        Input("default-filter-store", "data")
    )
    def update_js_support_status_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_js_support_status_summary(filters)
        return render_js_support_status_chart(df)

    @app.callback(
        Output("go-support-status-chart", "figure"),
        Input("default-filter-store", "data")
    )
    def update_go_support_status_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_go_support_status_summary(filters)
        return render_go_support_status_chart(df)



    generate_redirect_callbacks(
        app,
        target_href="/table-build-info",
        button_id="build-info-table-btn",
        output_container_id="build-info-table-link-container",
        reverse_href="/build-info",
        reverse_button_id="back-to-charts-btn-build-info",
    )

