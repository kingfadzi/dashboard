import pandas as pd
from dash import Input, Output, State, callback, dcc
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


def build_column_defs():
    return [
        {"headerName": "Repo Link", "field": "repo_link", "cellRenderer": "markdown"},
        {"headerName": "App Link", "field": "app_link", "cellRenderer": "markdown"},
        {"headerName": "Classification Label", "field": "classification_label"},
        {"headerName": "Transaction Cycle", "field": "transaction_cycle"},
        {"headerName": "Activity Status", "field": "activity_status"},
        {"headerName": "Main Language", "field": "main_language"},
        {"headerName": "All Languages", "field": "all_languages"},
        {
            "headerName": "Size",
            "field": "Size",
            "type": ["numericColumn", "rightAligned"],
            "sortByColumn": "repo_size_bytes"
        },
        {
            "headerName": "Age",
            "field": "Age",
            "type": ["numericColumn", "rightAligned"],
            "sortByColumn": "repo_age_days"
        },
        {
            "headerName": "Last Commit",
            "field": "Last Commit",
            "sortByColumn": "last_commit_ts"
        },
        {"headerName": "Total LOC", "field": "total_loc", "type": ["numericColumn", "rightAligned"]},
        {"headerName": "Total Commits", "field": "total_commits", "type": ["numericColumn", "rightAligned"]},
        {"headerName": "Contributors", "field": "number_of_contributors", "type": ["numericColumn", "rightAligned"]},
    ]


def register_modal_table_callbacks(
        app,
        table_id="modal-table",
        trigger_store_id="filters-applied-trigger",
        total_id="modal-total",
        download_id="download-all",
        download_btn_id="download-all-btn",
        modal_id="modal",
        open_btn_id="modal-open",
        close_btn_id="modal-close"
):
    @callback(
        Output(trigger_store_id, "data"),
        Input(open_btn_id, "n_clicks"),
        prevent_initial_call=True,
    )
    def trigger_filters_apply(n_clicks):
        return {"triggered": True}

    @app.callback(
        Output(table_id, "rowData"),
        Output(table_id, "columnDefs"),
        Output(total_id, "children"),
        Output(total_id, "is_open"),
        Input(trigger_store_id, "data"),
        State("host-name-filter", "value"),
        State("activity-status-filter", "value"),
        State("tc-filter", "value"),
        State("language-filter", "value"),
        State("classification-filter", "value"),
        State("app-id-filter", "value"),
        State(modal_id, "is_open"),
        prevent_initial_call=True,
    )
    def load_modal_data(trigger, hostnames, activities, tcs, langs, classifications, app_id, is_open):
        filters = {
            "host_name": hostnames or [],
            "activity_status": activities or [],
            "transaction_cycle": tcs or [],
            "main_language": langs or [],
            "classification_label": classifications or [],
            "app_id": app_id or "",
        }

        where_clause, params = build_repo_filter_conditions(filters)
        stmt = build_repo_modal_query(f" AND {where_clause}" if where_clause else "")
        df = pd.read_sql(stmt, engine, params=params)

        df["repo_link"] = df.apply(lambda r: f"[{r.repo_id}]({r.browse_url})", axis=1)
        df["app_link"] = df.apply(lambda r: f"[{r.app_id}](/repo?repo_id={r.repo_id})", axis=1)
        df["Size"] = df["repo_size_bytes"].apply(lambda b: f"{b / (1024 ** 2):,.1f} MB" if pd.notnull(b) else "")
        df["Age"] = df["repo_age_days"].apply(lambda d: f"{int(d) // 365} yr" if d >= 365 else f"{int(d) // 30} mo" if d >= 30 else f"{int(d)} d")
        df["Last Commit"] = pd.to_datetime(df["last_commit_date"], errors="coerce").dt.strftime("%b %d, %Y")
        df["last_commit_ts"] = pd.to_datetime(df["last_commit_date"], errors="coerce").astype("int64") // 10**9

        df = df[
            [
                "repo_link", "app_link", "classification_label", "transaction_cycle", "activity_status",
                "main_language", "all_languages",
                "repo_size_bytes", "Size",
                "repo_age_days", "Age",
                "last_commit_date", "Last Commit", "last_commit_ts",
                "total_loc", "total_commits", "number_of_contributors"
            ]
        ]

        column_defs = build_column_defs()
        return df.to_dict("records"), column_defs, f"{len(df):,} repositories matched.", True

    @app.callback(
        Output(download_id, "data"),
        Input(download_btn_id, "n_clicks"),
        State("host-name-filter", "value"),
        State("activity-status-filter", "value"),
        State("tc-filter", "value"),
        State("language-filter", "value"),
        State("classification-filter", "value"),
        State("app-id-filter", "value"),
        prevent_initial_call=True,
    )
    def download_all_repos(n_clicks, hostnames, activities, tcs, langs, classifications, app_id):
        if not n_clicks:
            raise PreventUpdate

        filters = {
            "host_name": hostnames or [],
            "activity_status": activities or [],
            "transaction_cycle": tcs or [],
            "main_language": langs or [],
            "classification_label": classifications or [],
            "app_id": app_id or "",
        }

        where_clause, params = build_repo_filter_conditions(filters)
        stmt = build_repo_modal_query(f" AND {where_clause}" if where_clause else "", limit=1000)
        df = pd.read_sql(stmt, engine, params=params)
        df = df.drop(columns=["repo_slug", "browse_url"], errors="ignore")
        return dcc.send_data_frame(df.to_csv, filename="repositories.csv", index=False)

    @app.callback(
        Output(modal_id, "is_open"),
        [Input(open_btn_id, "n_clicks"), Input(close_btn_id, "n_clicks")],
        State(modal_id, "is_open"),
        prevent_initial_call=True,
    )
    def toggle_modal(n1, n2, is_open):
        return not is_open if (n1 or n2) else is_open
