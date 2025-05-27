# callbacks/modal_table_callbacks.py

import pandas as pd
from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate
from sqlalchemy import text
from data.db_connection import engine
from data.sql_filter_utils import build_repo_filter_conditions


def register_modal_table_callbacks(app,
                                   modal_id="modal",
                                   open_btn_id="modal-open",
                                   close_btn_id="modal-close",
                                   table_id="modal-table",
                                   total_id="modal-total",
                                   filter_store_id="default-filter-store",
                                   trigger_store_id="filters-applied-trigger"):

    @callback(
        Output("default-filter-store", "data"),
        Input("language-filter",         "value"),
        Input("activity-status-filter", "value"),
        Input("tc-filter",              "value"),
        Input("classification-filter",  "value"),
        Input("app-id-filter",          "value"),
        Input("host-name-filter",       "value"),
    )
    def update_filter_store(main_language,
                            activity_status,
                            transaction_cycle,
                            classification_label,
                            app_id,
                            host_name):
        filters = {}
        if main_language:
            filters["main_language"] = main_language
        if activity_status:
            filters["activity_status"] = activity_status
        if transaction_cycle:
            filters["transaction_cycle"] = transaction_cycle
        if classification_label:
            filters["classification_label"] = classification_label
        if app_id:
            filters["app_id"] = app_id
        if host_name:
            filters["host_name"] = host_name

        return filters


    @callback(
        Output("filters-applied-trigger", "data"),
        Input("default-filter-store", "data"),
        prevent_initial_call=True
    )
    def sync_filters_applied_trigger(filters):
        if not filters:
            raise PreventUpdate
        return {"updated": True}

    # 3) Toggle the modal open/closed on button clicks
    @callback(
        Output("modal", "is_open"),
        Input("modal-open",  "n_clicks"),
        Input("modal-close", "n_clicks"),
        State("modal",       "is_open"),
        prevent_initial_call=True
    )
    def toggle_modal(n_open, n_close, is_open):
        if n_open:
            return True
        if n_close:
            return False
        raise PreventUpdate

    # 4) Load the table whenever the modal opens and filters are applied
    @callback(
        Output("modal-table",   "data"),
        Output("modal-table",   "columns"),
        Output("modal-total",   "children"),
        Output("modal-total",   "is_open"),
        Input("modal",          "is_open"),
        Input("filters-applied-trigger", "data"),
        State("default-filter-store",    "data"),
    )
    def load_modal_table(is_open, trigger, filters):
        if not is_open or not trigger or not filters:
            raise PreventUpdate

        # build WHERE clause + params
        where_clause, params = build_repo_filter_conditions(filters)
        extra = f" AND {where_clause}" if where_clause else ""

        # fetch all matching rows (client‐side paging/sorting)
        stmt = text(f"""
            SELECT
              hr.repo_id,
              hr.repo_slug,
              hr.app_id,
              hr.classification_label,
              hr.main_language,
              hr.all_languages,
              hr.activity_status
            FROM harvested_repositories hr
            LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id
            WHERE TRUE {extra}
            ORDER BY hr.repo_id DESC
        """)
        df = pd.read_sql(stmt, engine, params=params)

        data = df.to_dict("records")
        columns = [{"name": c, "id": c} for c in df.columns]
        total = len(df)
        total_msg = f"{total:,} repositories matched."

        return data, columns, total_msg, True
