# callbacks/filter_callbacks.py

from dash import Output, Input
from data.fetch_dropdown_options import fetch_dropdown_options

def register_filter_callbacks(app):
    @app.callback(
        [
            Output("host-name-filter", "options"),
            Output("activity-status-filter", "options"),
            Output("tc-filter", "options"),
            Output("language-filter", "props"),  # changed for ReactComponent
            Output("classification-filter", "options"),
        ],
        Input("_pages_location", "pathname"),
        allow_duplicate=True,
        prevent_initial_call=True,
    )
    def populate_dropdown_options(pathname):
        print(f"[populate_dropdown_options] triggered with pathname: {pathname}")
        opts = fetch_dropdown_options()
        print(f"[populate_dropdown_options] fetch_dropdown_options returned: {opts!r}")

        host_names = opts.get("host_names", [])
        statuses = opts.get("activity_statuses", [])
        tcs = opts.get("tcs", [])
        languages = opts.get("languages", [])
        classifications = opts.get("classification_labels", [])

        # For react-select, we return options via props
        language_props = {
            "options": [{"label": l, "value": l} for l in languages]
        }

        return (
            [{"label": h, "value": h} for h in host_names],
            [{"label": s, "value": s} for s in statuses],
            [{"label": tc, "value": tc} for tc in tcs],
            language_props,
            [{"label": c, "value": c} for c in classifications],
        )
