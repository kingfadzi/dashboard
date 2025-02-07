import dash_bootstrap_components as dbc
from dash import html

def kpi_layout():
    return dbc.Row(
        [
            # Total Repos (one output)
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Total Repos",
                            className="text-center bg-light",
                            style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}
                        ),
                        dbc.CardBody(
                            html.H4("0", id="kpi-total-repos", className="text-center", style={"whiteSpace": "nowrap"})
                        ),
                    ],
                    className="mb-4",
                ),
            ),
            # Avg Commits (two outputs)
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Avg Commits",
                            className="text-center bg-light",
                            style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}
                        ),
                        dbc.CardBody(
                            [
                                html.H4("0", id="kpi-avg-commits", className="text-center mb-1", style={"whiteSpace": "nowrap"}),
                                html.Small("Min=0 | Max=0", id="kpi-avg-commits-subtext",
                                           className="text-center text-muted d-block", style={"whiteSpace": "nowrap"}),
                            ]
                        ),
                    ],
                    className="mb-4",
                ),
            ),
            # Avg Contributors (two outputs)
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Avg Contributors",
                            className="text-center bg-light",
                            style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}
                        ),
                        dbc.CardBody(
                            [
                                html.H4("0", id="kpi-avg-contributors", className="text-center mb-1", style={"whiteSpace": "nowrap"}),
                                html.Small("Min=0 | Max=0", id="kpi-avg-contributors-subtext",
                                           className="text-center text-muted d-block", style={"whiteSpace": "nowrap"}),
                            ]
                        ),
                    ],
                    className="mb-4",
                ),
            ),
            # Avg Lines of Code (two outputs)
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Avg Lines of Code",
                            className="text-center bg-light",
                            style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}
                        ),
                        dbc.CardBody(
                            [
                                html.H4("0", id="kpi-avg-loc", className="text-center mb-1", style={"whiteSpace": "nowrap"}),
                                html.Small("Min=0 | Max=0", id="kpi-avg-loc-subtext",
                                           className="text-center text-muted d-block", style={"whiteSpace": "nowrap"}),
                            ]
                        ),
                    ],
                    className="mb-4",
                ),
            ),
            # Avg CCN (two outputs)
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Avg CCN",
                            className="text-center bg-light",
                            style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}
                        ),
                        dbc.CardBody(
                            [
                                html.H4("0", id="kpi-avg-ccn", className="text-center mb-1", style={"whiteSpace": "nowrap"}),
                                html.Small("Tokens=0 | Fn=0 | Total CCN=0", id="kpi-ccn-subtext",
                                           className="text-center text-muted d-block", style={"whiteSpace": "nowrap"}),
                            ]
                        ),
                    ],
                    className="mb-4",
                ),
            ),
            # Avg Repo Size (two outputs)
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Avg Repo Size",
                            className="text-center bg-light",
                            style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}
                        ),
                        dbc.CardBody(
                            [
                                html.H4("0", id="kpi-avg-repo-size", className="text-center mb-1", style={"whiteSpace": "nowrap"}),
                                html.Small("Min=0 | Max=0", id="kpi-avg-repo-size-subtext",
                                           className="text-center text-muted d-block", style={"whiteSpace": "nowrap"}),
                            ]
                        ),
                    ],
                    className="mb-4",
                ),
            ),
            # Dockerfiles (two outputs)
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Dockerfiles",
                            className="text-center bg-light",
                            style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}
                        ),
                        dbc.CardBody(
                            [
                                html.H4("0", id="kpi-dockerfiles", className="text-center mb-1", style={"whiteSpace": "nowrap"}),
                                html.Small("Total=0", id="kpi-dockerfiles-subtext",
                                           className="text-center text-muted d-block", style={"whiteSpace": "nowrap"}),
                            ]
                        ),
                    ],
                    className="mb-4",
                ),
            ),
        ],
        rowCols=7,
        className="mb-4",
    )