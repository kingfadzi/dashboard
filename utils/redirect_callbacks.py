import urllib.parse
from dash import Input, Output, State, callback, dcc
from utils.filter_utils import FILTER_STATES, extract_filter_dict

def generate_redirect_callbacks(app, target_href, button_id, output_container_id, reverse_href, reverse_button_id):
    @app.callback(
        Output(output_container_id, "children", allow_duplicate=True),
        Input(button_id, "n_clicks"),
        *FILTER_STATES,
        prevent_initial_call=True,
    )
    def _apply_filters_and_redirect(n_clicks, *vals):
        filters = extract_filter_dict(*vals)
        query = urllib.parse.urlencode(filters, doseq=True)
        return dcc.Location(href=f"{target_href}?{query}", id="redirect-location", refresh=True)

    @app.callback(
        Output(output_container_id, "children", allow_duplicate=True),
        Input(reverse_button_id, "n_clicks"),
        *FILTER_STATES,
        prevent_initial_call=True,
    )
    def _go_back_to_charts(n_clicks, *vals):
        filters = extract_filter_dict(*vals)
        query = urllib.parse.urlencode(filters, doseq=True)
        return dcc.Location(href=f"{reverse_href}?{query}", id="redirect-location", refresh=True)

