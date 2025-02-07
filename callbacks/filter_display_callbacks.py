from dash import Input, Output

def register_filter_display_callback(app):
    @app.callback(
        Output("current-filters", "children"),
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
        ]
    )
    def update_filter_display(host, status, tc, language, classification):
        filters = []
        # Only add the filter text if the filter is set and not the default (e.g., "all")
        if host and host != "all":
            filters.append(f"Host: {host}")
        if status and status != "all":
            filters.append(f"Status: {status}")
        if tc and tc != "all":
            filters.append(f"TC: {tc}")
        if language and language != "all":
            filters.append(f"Language: {language}")
        if classification and classification != "all":
            filters.append(f"Classification: {classification}")

        if filters:
            return " | ".join(filters)
        else:
            return "No filters applied"