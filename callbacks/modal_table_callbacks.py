# callbacks/modal_table_callbacks.py

import pandas as pd
from dash import Input, Output, State, callback, ctx, dcc
from dash.exceptions import PreventUpdate
from sqlalchemy import text
from data.db_connection import engine
from data.sql_filter_utils import build_repo_filter_conditions

def register_modal_table_callbacks(
        app,
        modal_id="modal",
        open_btn_id="modal-open",
        close_btn_id="modal-close",
        table_id="modal-table",
        total_id="modal-total",
        filter_store_id="default-filter-store",
        trigger_store_id="filters-applied-trigger"
):

    # 1) Update the shared filter store
    @app.callback(
        Output(filter_store_id, "data"),
        Input("language-filter",         "value"),
        Input("activity-status-filter", "value"),
        Input("tc-filter",              "value"),
        Input("classification-filter",  "value"),
        Input("app-id-filter",          "value"),
        Input("host-name-filter",       "value"),
    )
    def _update_filter_store(
            main_language,
            activity_status,
            transaction_cycle,
            classification_label,
            app_id,
            host_name
    ):
        filters = {}
        if main_language:
            filters["main_language"]       = main_language
        if activity_status:
            filters["activity_status"]     = activity_status
        if transaction_cycle:
            filters["transaction_cycle"]   = transaction_cycle
        if classification_label:
            filters["classification_label"] = classification_label
        if app_id:
            filters["app_id"]              = app_id
        if host_name:
            filters["host_name"]           = host_name
        return filters

    # 2) Emit a "filters applied" trigger
    @app.callback(
        Output(trigger_store_id, "data"),
        Input(filter_store_id, "data"),
        prevent_initial_call=True
    )
    def _sync_filters_applied_trigger(filters):
        if not filters:
            raise PreventUpdate
        return {"updated": True}

    # 3) Toggle the modal open/close
    @app.callback(
        Output(modal_id, "is_open"),
        Input(open_btn_id,  "n_clicks"),
        Input(close_btn_id, "n_clicks"),
        State(modal_id,     "is_open"),
        prevent_initial_call=True
    )
    def _toggle_modal(n_open, n_close, is_open):
        triggered = ctx.triggered_id
        if triggered == open_btn_id:
            return True
        if triggered == close_btn_id:
            return False
        raise PreventUpdate

    # 4) Load and format the table when the modal opens and filters applied
    @app.callback(
        Output(table_id, "data"),
        Output(table_id, "columns"),
        Output(total_id, "children"),
        Output(total_id, "is_open"),
        Input(modal_id,            "is_open"),
        Input(trigger_store_id,    "data"),
        State(filter_store_id,     "data"),
    )
    def _load_modal_table(is_open, trigger, filters):
        if not is_open or not trigger or not filters:
            raise PreventUpdate

        # Build WHERE clause + params
        where_clause, params = build_repo_filter_conditions(filters)
        extra = f" AND {where_clause}" if where_clause else ""

        # Fetch all matching rows
        stmt = text(f"""
            SELECT
              hr.repo_id,
              hr.repo_slug,
              hr.app_id,
              hr.browse_url,
              hr.host_name,
              hr.transaction_cycle,
              hr.classification_label,
              hr.main_language,
              hr.all_languages,
              hr.activity_status,
              rm.repo_age_days,
              rm.last_commit_date,
              rm.number_of_contributors,
              rm.total_commits,
              rm.repo_size_bytes
            FROM harvested_repositories hr
            LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id
            WHERE TRUE {extra}
            ORDER BY hr.repo_id DESC
        """)
        df = pd.read_sql(stmt, engine, params=params)

        # Keep a copy of raw repo_id for linking
        df["raw_repo_id"] = df["repo_id"]

        # Format repo_id as external “browse” link
        df["repo_id"] = df.apply(
            lambda row: (
                f'<a href="{row["browse_url"]}" target="_blank">'
                f'{row["raw_repo_id"]}</a>'
            ),
            axis=1
        )

        # Format app_id as internal link to repo profile using the raw repo_id
        df["app_id"] = df.apply(
            lambda row: (
                f'<a href="/repo?repo_id={row["raw_repo_id"]}" target="_blank">'
                f'{row["app_id"]}</a>'
            ),
            axis=1
        )

        # Drop helper and unused columns
        df = df.drop(columns=["repo_slug", "browse_url", "host_name", "raw_repo_id", "main_language"])

        # Prepare DataTable outputs with markdown presentation
        data = df.to_dict("records")
        columns = [
            {"name": col.replace("_", " ").title(), "id": col, "presentation": "markdown"}
            for col in df.columns
        ]
        total = len(df)
        total_msg = f"{total:,} repositories matched."

        return data, columns, total_msg, True

    # 5) Download up to 500 rows as CSV
    @app.callback(
        Output("download-all", "data"),
        Input("download-all-btn", "n_clicks"),
        State(filter_store_id, "data"),
        prevent_initial_call=True,
    )
    def download_all_repos(n_clicks, filters):
        if not n_clicks or not filters:
            raise PreventUpdate

        # Rebuild WHERE clause from the current filters
        where_clause, params = build_repo_filter_conditions(filters)
        extra = f" AND {where_clause}" if where_clause else ""

        # Pull up to 500 rows server‐side
        stmt = text(f"""
            SELECT
                hr.repo_id,
                hr.repo_slug,
                hr.app_id,
                hr.browse_url,
                hr.host_name,
                hr.transaction_cycle,
                hr.classification_label,
                hr.main_language,
                hr.all_languages,
                hr.activity_status
            FROM harvested_repositories hr
            LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id
            WHERE TRUE {extra}
            ORDER BY hr.repo_id DESC
            LIMIT 500
        """)
        df = pd.read_sql(stmt, engine, params=params)

        # Drop raw slug/URL columns if still present
        df = df.drop(columns=["repo_slug", "browse_url"], errors="ignore")

        # Stream as CSV
        return dcc.send_data_frame(df.to_csv, filename="repositories.csv", index=False)
