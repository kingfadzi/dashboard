from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate
from urllib.parse import parse_qs
from pages.repo_profile import render_repo_profile_content
from dash import html
import dash_bootstrap_components as dbc

def register_repo_modal_callbacks(app):
    @app.callback(
        Output("repo-modal-container", "children"),
        Input("repo-modal-location", "search"),
        prevent_initial_call=True,
    )
    def open_repo_modal(search):
        if not search:
            raise PreventUpdate

        repo_id = parse_qs(search.lstrip("?")).get("repo_id", [None])[0]
        if not repo_id:
            raise PreventUpdate

        return dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(f"Repository: {repo_id}")),
                dbc.ModalBody(render_repo_profile_content(repo_id)),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-repo-modal", className="ms-auto")
                ),
            ],
            id="repo-details-modal",
            is_open=True,
            size="xl",
            scrollable=True,
            backdrop="static",
        )

    @app.callback(
        Output("repo-modal-container", "children", allow_duplicate=True),
        Input("close-repo-modal", "n_clicks"),
        prevent_initial_call=True,
    )
    def close_repo_modal(n):
        return ""