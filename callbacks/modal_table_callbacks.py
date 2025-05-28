import pandas as pd
from dash import Input, Output, State, callback, ctx, dcc
from dash.exceptions import PreventUpdate
from dash_ag_grid import GridOptionsBuilder
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


def register_modal_table_callbacks_aggrid(
        app,
        table_id="modal-table",
        filter_store_id="default-filter-store",
        trigger_store_id="filters-applied-trigger",
        total_id="modal-total",
        download_id="download-all",
        download_btn_id="download-all-btn"
):
    @app.callback(
        Output(table_id, "rowData"),
        Output(table_id, "columnDefs"),
        Output(total_id, "children"),
        Output(total_id, "is_open"),
        Input(trigger_store_id, "data"),
        State(filter_store_id, "data"),
    )
    def _load_ag_grid(trigger, filters):
        if not trigger or not filters:
            raise PreventUpdate

        where_clause, params = build_repo_filter_conditions(filters)
        stmt = build_repo_modal_query(f" AND {where_clause}" if where_clause else "")
        df = pd.read_sql(stmt, engine, params=params)

        # Render links
        df["repo_link"] = df.apply(lambda r: f"[{r.repo_id}]({r.browse_url})", axis=1)
        df["app_link"] = df.apply(lambda r: f"[{r.app_id}](/repo?repo_id={r.repo_id})", axis=1)

        # Format fields
        df["Size"] = df["repo_size_bytes"].apply(lambda b: f"{b / (1024**2):,.1f} MB" if pd.notnull(b) else "")
        df["Age"] = df["repo_age_days"].apply(lambda d: f"{int(d)//365} yr" if d >= 365 else f"{int(d)//30} mo" if d >= 30 else f"{int(d)} d")
        df["Last Commit"] = pd.to_datetime(df["last_commit_date"], errors="coerce").dt.strftime("%b %d, %Y")
        df["Total LOC"] = df["total_loc"]
        df["Total Commits"] = df["total_commits"]
        df["Contributors"] = df["number_of_contributors"]

        # Final columns
        df = df[[
            "repo_link", "app_link", "classification_label", "transaction_cycle", "activity_status",
            "main_language", "all_languages", "Size", "Age", "Last Commit",
            "Total LOC", "Total Commits", "Contributors"
        ]]

        # AG Grid config
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(resizable=True, sortable=True, filter=True, wrapText=True, autoHeight=True)
        gb.configure_column("repo_link", headerName="Repo ID", cellRenderer="markdown")
        gb.configure_column("app_link", headerName="App ID", cellRenderer="markdown")

        for col in ["Total LOC", "Total Commits", "Contributors"]:
            gb.configure_column(col, type=["numericColumn", "rightAligned"])

        return df.to_dict("records"), gb.build()["columnDefs"], f"{len(df):,} repositories matched.", True

    @app.callback(
        Output(download_id, "data"),
        Input(download_btn_id, "n_clicks"),
        State(filter_store_id, "data"),
        prevent_initial_call=True,
    )
    def download_all_repos(n_clicks, filters):
        if not n_clicks or not filters:
            raise PreventUpdate

        where_clause, params = build_repo_filter_conditions(filters)
        stmt = build_repo_modal_query(f" AND {where_clause}" if where_clause else "", limit=500)
        df = pd.read_sql(stmt, engine, params=params)
        df = df.drop(columns=["repo_slug", "browse_url"], errors="ignore")
        return dcc.send_data_frame(df.to_csv, filename="repositories.csv", index=False)