from dash import Input, Output, State, html

def register_language_filter_callbacks(app):
    # Toggle visibility of the real dropdown when summary is clicked
    @app.callback(
        Output("language-filter-visible", "data"),
        Input("language-filter-display", "n_clicks"),
        State("language-filter-visible", "data"),
        prevent_initial_call=True
    )
    def toggle_dropdown(n_clicks, visible):
        return not visible

    # Show or hide the editable dropdown
    @app.callback(
        Output("language-filter-dropdown-container", "style"),
        Input("language-filter-visible", "data")
    )
    def show_real_dropdown(visible):
        return {"display": "block"} if visible else {"display": "none"}

    # ✅ Sync real → hidden with allow_duplicate to prevent Dash error
    @app.callback(
        Output("language-filter", "value"),
        Input("language-filter-real", "value"),
        allow_duplicate=True
    )
    def sync_real_to_hidden(val):
        return val

    # Render [X] [Y] [+N more] summary in compact display
    @app.callback(
        Output("language-filter-display", "children"),
        Input("language-filter", "value"),
        State("language-filter", "options")
    )
    def show_display_summary(selected, options):
        if not selected:
            return "Select Language(s) ▼"

        max_display = 2
        labels = [next((o["label"] for o in options if o["value"] == v), v) for v in selected]
        display_items = labels[:max_display]
        extra_count = len(labels) - max_display

        pills = [html.Span(l, className="badge bg-secondary me-1") for l in display_items]
        if extra_count > 0:
            pills.append(html.Span(f"+{extra_count} more", className="text-muted me-1"))

        pills.append(html.Span("▼", className="ms-auto"))
        return pills