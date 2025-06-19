# File: callbacks/status/status_callbacks.py
import logging
from dash import Input, Output
from dash.exceptions import PreventUpdate
from data.status.status_fetcher import fetch_status_kpis
from utils.filter_utils import extract_filter_dict_from_store

def register_status_callbacks(app):
    logger = logging.getLogger(__name__)

    @app.callback(
        Output("status-waiting-count", "children"),
        Output("status-in-progress-count", "children"),
        Output("status-completed-count", "children"),
        Output("status-failed-count", "children"),
        Input("url", "pathname"),
        Input("default-filter-store", "data"),
    )
    def update_status_counts(pathname, store_data):
        if pathname != "/status":
            raise PreventUpdate

        filters = extract_filter_dict_from_store(store_data or {})
        metrics = fetch_status_kpis(filters)
        logger.info(f"Fetched status metrics with filters {filters}: {metrics}")

        return (
            metrics.get("waiting",      0),
            metrics.get("in_progress",  0),
            metrics.get("completed",    0),
            metrics.get("failed",       0),
        )
