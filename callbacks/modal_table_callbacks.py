import pandas as pd
from dash import Input, Output, State, callback, ctx, dcc
from dash.exceptions import PreventUpdate
from sqlalchemy import text
from data.db_connection import engine
from data.sql_filter_utils import build_repo_filter_conditions


def build_repo_modal_query(extra_clause: str = "", limit: int = None):
    query = f"""
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
          rm.repo_size_bytes,
          COALESCE(cm.total_loc, 0) AS total_loc
        FROM harvested_repositories hr
        LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id
        LEFT JOIN (
            SELECT repo_id, SUM(code) AS total_loc
            FROM cloc_metrics
            GROUP BY repo_id
        ) cm ON hr.repo_id = cm.repo_id
        WHERE TRUE {extra_clause}
        ORDER BY rm.last_commit_date DESC
    """
    if limit:
        query += f" LIMIT {limit}"
    return text(query)


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

    @app.callback(
        Output(filter_store_id, "data"),
        Input("language-filter",         "value"),
        Input("activity-status-filter", "value"),
        Input("tc-filter",              "value"),
        Input("classification-filter",  "value"),
        Input("app-id-filter",          "value"),
        Input("host-name-filter",       "value"),
    )
    def _update_filter_store(main_language, activity_status, transaction_cycle, classification_label, app_id, host_name):
        filters = {}
        if main_language: filters["main_language"] = main_language
        if activity_status: filters["activity_status"] = activity_status
        if transaction_cycle: filters["transaction_cycle"] = transaction_cycle
        if classification_label: filters["classification_label"] = classification_label
        if app_id: filters["app_id"] = app_id
        if host_name: filters["host_name"] = host_name
        return filters

    @app.callback(
        Output(trigger_store_id, "data"),
        Input(filter_store_id, "data"),
        prevent_initial_call=True
    )
    def _sync_filters_applied_trigger(filters):
        if not filters:
            raise PreventUpdate
        return {"updated": True}

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

        where_clause, params = build_repo_filter_conditions(filters)
        extra = f" AND {where_clause}" if where_clause else ""
        stmt = build_repo_modal_query(extra)
        df = pd.read_sql(stmt, engine, params=params)

        df["raw_repo_id"] = df["repo_id"]

        df["repo_id"] = df.apply(
            lambda row: (
                f'<a href="{row["browse_url"]}" target="_blank">'
                f'{row["raw_repo_id"]}</a>'
            ),
            axis=1
        )

        df["app_id"] = df.apply(
            lambda row: (
                f'<a href="/repo?repo_id={row["raw_repo_id"]}" target="_blank">'
                f'{row["app_id"]}</a>'
            ),
            axis=1
        )

        df["all_languages"] = df["all_languages"].apply(
            lambda langs: ", ".join(langs.split(", ")[:5]) + "..." if langs and len(langs.split(", ")) > 5 else langs
        )

        def format_bytes(b):
            if b is None:
                return "0 B"
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if b < 1024:
                    return f"{b:.1f} {unit}"
                b /= 1024
            return f"{b:.1f} PB"

        df["repo_size"] = df["repo_size_bytes"].apply(format_bytes)
        df.drop(columns=["repo_size_bytes"], inplace=True)

        df["last_commit_date"] = pd.to_datetime(df["last_commit_date"], errors="coerce").dt.strftime("%b %d, %Y")

        df["repo_age_days"] = df["repo_age_days"].apply(
            lambda d: f"{int(d)//365} yr" if d >= 365 else f"{int(d)//30} mo" if d >= 30 else f"{int(d)} d"
        )

        df["total_commits"] = df["total_commits"].apply(lambda x: f"{int(x):,}" if pd.notnull(x) else "")
        df["number_of_contributors"] = df["number_of_contributors"].apply(lambda x: f"{int(x):,}" if pd.notnull(x) else "")
        df["total_loc"] = df["total_loc"].apply(lambda x: f"{int(x):,}" if pd.notnull(x) else "")

        df = df.drop(columns=["repo_slug", "browse_url", "host_name", "raw_repo_id", "main_language"])

        column_name_map = {
            "classification_label": "Classification",
            "repo_age_days": "Age",
            "last_commit_date": "Last Commit",
            "number_of_contributors": "Contributors",
            "repo_size": "Size",
            "total_loc": "Total LOC"
        }

        data = df.to_dict("records")
        columns = [
            {
                "name": column_name_map.get(col, col.replace("_", " ").title()),
                "id": col,
                "presentation": "markdown" if col in ["repo_id", "app_id"] else "input"
            }
            for col in df.columns
        ]
        total_msg = f"{len(df):,} repositories matched."
        return data, columns, total_msg, True

    @app.callback(
        Output("download-all", "data"),
        Input("download-all-btn", "n_clicks"),
        State(filter_store_id, "data"),
        prevent_initial_call=True,
    )
    def download_all_repos(n_clicks, filters):
        if not n_clicks or not filters:
            raise PreventUpdate

        where_clause, params = build_repo_filter_conditions(filters)
        extra = f" AND {where_clause}" if where_clause else ""
        stmt = build_repo_modal_query(extra, limit=500)
        df = pd.read_sql(stmt, engine, params=params)
        df = df.drop(columns=["repo_slug", "browse_url"], errors="ignore")
        return dcc.send_data_frame(df.to_csv, filename="repositories.csv", index=False)
