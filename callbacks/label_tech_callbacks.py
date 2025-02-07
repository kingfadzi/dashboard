# label_tech_callbacks.py
from dash import Input, Output
from data.fetch_label_tech_data import fetch_label_tech_data
from callbacks.viz_label_tech import viz_label_tech

def register_label_tech_callbacks(app):
    @app.callback(
        [
            Output("label-tech-bar-chart-java-version", "figure"),
            Output("label-tech-bar-chart-build-tool", "figure"),
            Output("label-tech-bar-chart-appserver", "figure"),
            Output("label-tech-bar-chart-database", "figure"),
            Output("label-tech-bar-chart-spring-framework-version", "figure"),
            Output("label-tech-bar-chart-spring-boot-version", "figure"),
            Output("label-tech-bar-chart-middleware", "figure"),
            Output("label-tech-bar-chart-logging", "figure"),
        ],
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
        ],
    )
    def update_label_tech(*args):
        filter_keys = [
            "host_name",
            "activity_status",
            "tc",
            "main_language",
            "classification_label",
            "app_id",
        ]
        filters = {key: (arg if arg else None) for key, arg in zip(filter_keys, args)}
        fig_java = viz_label_tech(fetch_label_tech_data(filters, "cto.io/java-version"))
        fig_build = viz_label_tech(fetch_label_tech_data(filters, "cto.io/build-tool"))
        fig_appserver = viz_label_tech(fetch_label_tech_data(filters, "cto.io/appserver"))
        fig_database = viz_label_tech(fetch_label_tech_data(filters, "cto.io/database"))
        fig_spring_fw = viz_label_tech(fetch_label_tech_data(filters, "cto.io/spring-framework-version"))
        fig_spring_boot = viz_label_tech(fetch_label_tech_data(filters, "cto.io/spring-boot-version"))
        fig_middleware = viz_label_tech(fetch_label_tech_data(filters, "cto.io/middleware"))
        fig_logging = viz_label_tech(fetch_label_tech_data(filters, "cto.io/logging"))
        
        return (
            fig_java,
            fig_build,
            fig_appserver,
            fig_database,
            fig_spring_fw,
            fig_spring_boot,
            fig_middleware,
            fig_logging,
        )