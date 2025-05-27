from dash import Input, Output
from data.fetch_dropdown_options import fetch_dropdown_options

def register_filter_callbacks(app):
    @app.callback(
        [
            Output("host-name-filter", "options"),
            Output("activity-status-filter", "options"),
            Output("tc-filter", "options"),
            Output("language-filter", "options"),
            Output("classification-filter", "options"),
        ],
        Input("_pages_location", "pathname"),
    )
    def populate_dropdown_options(pathname):
        print(f"[populate_dropdown_options] triggered with pathname: {pathname}")
        opts = fetch_dropdown_options()
        print(f"[populate_dropdown_options] fetch_dropdown_options returned: {opts!r}")
        # Defensive defaults if keys missing
        host_names   = opts.get("host_names", [])
        statuses     = opts.get("activity_statuses", [])
        tcs          = opts.get("tcs", [])
        languages    = opts.get("languages", [])
        classifications = opts.get("classification_labels", [])

        return (
            [{"label": n, "value": n} for n in host_names],
            [{"label": s, "value": s} for s in statuses],
            [{"label": tc, "value": tc} for tc in tcs],
            [{"label": lg, "value": lg} for lg in languages],
            [{"label": cl, "value": cl} for cl in classifications],
        )
