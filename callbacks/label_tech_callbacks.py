# label_tech_callbacks.py

import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
from data.fetch_label_tech_data import fetch_label_tech_data
from viz.viz_label_tech import viz_label_tech

# Helper function: only used in this file.
def create_label_tech_rows(
    fig_java, fig_build, fig_appserver, fig_database,
    fig_spring_fw, fig_spring_boot, fig_middleware, fig_logging,
    height=300
):
    # List of chart definitions.
    charts = [
        {"title": "Java Versions", "id": "label-tech-bar-chart-java-version", "figure": fig_java},
        {"title": "Build Tools", "id": "label-tech-bar-chart-build-tool", "figure": fig_build},
        {"title": "Appserver", "id": "label-tech-bar-chart-appserver", "figure": fig_appserver},
        {"title": "Database", "id": "label-tech-bar-chart-database", "figure": fig_database},
        {"title": "Spring Framework", "id": "label-tech-bar-chart-spring-framework-version", "figure": fig_spring_fw},
        {"title": "Spring Boot", "id": "label-tech-bar-chart-spring-boot-version", "figure": fig_spring_boot},
        {"title": "Middleware", "id": "label-tech-bar-chart-middleware", "figure": fig_middleware},
        {"title": "Logging", "id": "label-tech-bar-chart-logging", "figure": fig_logging},
    ]

    # Helper to create a chart card only if the figure has data.
    def create_chart_card(chart):
        if not chart["figure"] or not chart["figure"].get("data"):
            return None
        card = dbc.Card(
            [
                dbc.CardHeader(
                    html.B(chart["title"], className="text-center"),
                    className="bg-light"
                ),
                dcc.Graph(
                    id=chart["id"],
                    figure=chart["figure"],
                    config={"displayModeBar": False},
                    style={"height": height},
                ),
            ],
            className="mb-4",
        )
        return dbc.Col(card, width=6)

    # Build a list of columns (cards) for charts that have data.
    cols = [create_chart_card(chart) for chart in charts]
    # Filter out any None values (charts with no data).
    cols = [col for col in cols if col is not None]

    # Group columns into rows with 2 columns per row.
    rows = []
    for i in range(0, len(cols), 2):
        row = dbc.Row(cols[i:i+2], className="mb-4")
        rows.append(row)
    return rows

def register_label_tech_callbacks(app):
    @app.callback(
        Output("label-tech-layout", "children"),  # This container is defined in your layout.
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
        ],
    )
    def update_label_tech_layout(host, status, tc, language, classification, app_id):
        # Build the filters dictionary.
        filters = {
            "host_name": host or None,
            "activity_status": status or None,
            "tc": tc or None,
            "main_language": language or None,
            "classification_label": classification or None,
            "app_id": app_id or None,
        }
        
        # Generate figures for each metric.
        fig_java      = viz_label_tech(fetch_label_tech_data(filters, "cto.io/java-version"))
        fig_build     = viz_label_tech(fetch_label_tech_data(filters, "cto.io/build-tool"))
        fig_appserver = viz_label_tech(fetch_label_tech_data(filters, "cto.io/appserver"))
        fig_database  = viz_label_tech(fetch_label_tech_data(filters, "cto.io/database"))
        fig_spring_fw = viz_label_tech(fetch_label_tech_data(filters, "cto.io/spring-framework-version"))
        fig_spring_boot = viz_label_tech(fetch_label_tech_data(filters, "cto.io/spring-boot-version"))
        fig_middleware  = viz_label_tech(fetch_label_tech_data(filters, "cto.io/middleware"))
        fig_logging     = viz_label_tech(fetch_label_tech_data(filters, "cto.io/logging"))
        
        # Create rows of charts (2 per row).
        rows = create_label_tech_rows(
            fig_java, fig_build, fig_appserver, fig_database,
            fig_spring_fw, fig_spring_boot, fig_middleware, fig_logging
        )
        return rows