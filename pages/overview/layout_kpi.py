import dash_bootstrap_components as dbc
from dash import html

def kpi_layout():
    def make_col(card):
        return dbc.Col(card, xs=6, sm=4, md=3, lg=2, className="mb-4")

    def make_card(title, value_id, subtext_id, subtext):
        return dbc.Card(
            [
                dbc.CardHeader(
                    title,
                    className="text-center bg-light",
                    style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}
                ),
                dbc.CardBody([
                    html.H4("0", id=value_id, className="text-center"),
                    html.Small(
                        subtext,
                        id=subtext_id,
                        className="text-center text-muted d-block",
                        style={
                            "fontSize": "0.7rem",
                            "whiteSpace": "nowrap",
                            "overflow": "hidden",
                            "textOverflow": "ellipsis"
                        }
                    )
                ])
            ]
        )


    return dbc.Row(
        [
            # Total Repos: default subtext updated
            make_col(make_card(
                "Total Repos",
                "kpi-total-repos",
                "kpi-total-repos-subtext",
                "With AppID:0 · Without:0"
            )),
            make_col(make_card("Updates",            "kpi-avg-commits",       "kpi-avg-commits-subtext",       "Recent:0 · 30d")),
            make_col(make_card("Oldest Repos",       "kpi-oldest-repos",      "kpi-oldest-repos-subtext",      ">3y:0 · 5y:0 · 10y:0")),
            make_col(make_card("Massive Repos",      "kpi-massive-repos",     "kpi-massive-repos-subtext",     "Code:0 · Data:0 · None:0")),
            make_col(make_card("Solo Devs",          "kpi-avg-contributors",  "kpi-avg-contributors-subtext",  "All:0")),
            make_col(make_card("LOC",                "kpi-avg-loc",           "kpi-avg-loc-subtext",           "Files:0 · Repos:0")),
            make_col(make_card("Branching Sprawl",   "kpi-branches",          "kpi-branches-subtext",          ">10 branches")),
            make_col(make_card("Build Tools",        "kpi-build-tools",       "kpi-build-tools-subtext",       "Modules:0 · NoTool:0")),
            make_col(make_card("Runtimes",           "kpi-runtime",           "kpi-runtime-subtext",           "Languages:0")),
            make_col(make_card("CI/CD",              "kpi-cicd",              "kpi-cicd-subtext",              "GL:0 · Jenkins:0")),
            make_col(make_card("Dockerfiles",        "kpi-container",         "kpi-container-subtext",         "Helm:0 · Compose:0")),
            make_col(make_card("Sources",            "kpi-sources",           "kpi-sources-subtext",           "GitLab:0 · Bitbucket:0")),
        ],
        className="mt-4 g-2",
        justify="start"
    )
