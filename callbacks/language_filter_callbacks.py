from dash import Input, Output, State, html

def register_language_filter_callbacks(app):
    @app.callback(
        Output("language-filter-visible", "data"),
        Input("language-filter-display", "n_clicks"),
        State("language-filter-visible", "data"),
        prevent_initial_call=True
    )
    def toggle_visibility(n_clicks, visible):
        return not visible

    @app.callback(
        Output("language-filter-dropdown-container", "style"),
        Input("language-filter-visible", "data")
    )
    def show_dropdown(visible):
        return {"display": "block"} if visible else {"display": "none"}

    @app.callback(
        Output("language-filter", "value"),
        Input("language-filter-real", "value"),
        allow_duplicate=True
    )
    def sync_real_to_display(val):
        return val

    @app.callback(
        Output("language-filter-display", "children"),
        Input("language-filter", "value"),
        State("language-filter", "options")
    )
    def render_summary(value, options):
        if not value:
            return "Select Language(s) ▼"
        max_display = 2
        labels = [next((o["label"] for o in options if o["value"] == v), v) for v in value]
        pills = [html.Span(label, className="badge bg-secondary me-1") for label in labels[:max_display]]
        if len(labels) > max_display:
            pills.append(html.Span(f"+{len(labels) - max_display} more", className="text-muted me-1"))
        pills.append(html.Span("▼", className="ms-auto"))
        return pills