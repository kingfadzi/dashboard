import dash_bootstrap_components as dbc
from dash import html

def kpi_layout():
    return dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Total Repos",
                            className="text-center bg-light",
                            style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}
                        ),
                        dbc.CardBody(
                            [
                                html.H4(
                                    "0",
                                    id="kpi-total-repos",
                                    className="text-center",
                                    style={"whiteSpace": "nowrap"}
                                ),
                                html.Small(
                                    "Total=0",
                                    id="kpi-total-repos-subtext",
                                    className="text-center text-muted d-block",
                                    style={"whiteSpace": "nowrap", "fontSize": "0.7rem"}
                                ),
                            ]
                        ),
                    ],
                    className="mb-4"
                )
            ),
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
                                html.H4(
                                    "0",
                                    id="kpi-dockerfiles",
                                    className="text-center mb-1",
                                    style={"whiteSpace": "nowrap"}
                                ),
                                html.Small(
                                    "Total=0",
                                    id="kpi-dockerfiles-subtext",
                                    className="text-center text-muted d-block",
                                    style={"whiteSpace": "nowrap", "fontSize": "0.7rem"}
                                ),
                            ]
                        ),
                    ],
                    className="mb-4"
                )
            ),
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
                                html.H4(
                                    "0",
                                    id="kpi-avg-commits",
                                    className="text-center mb-1",
                                    style={"whiteSpace": "nowrap"}
                                ),
                                html.Small(
                                    "Min=0 | Max=0",
                                    id="kpi-avg-commits-subtext",
                                    className="text-center text-muted d-block",
                                    style={"whiteSpace": "nowrap", "fontSize": "0.7rem"}
                                ),
                            ]
                        ),
                    ],
                    className="mb-4"
                )
            ),
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
                                html.H4(
                                    "0",
                                    id="kpi-avg-contributors",
                                    className="text-center mb-1",
                                    style={"whiteSpace": "nowrap"}
                                ),
                                html.Small(
                                    "Min=0 | Max=0",
                                    id="kpi-avg-contributors-subtext",
                                    className="text-center text-muted d-block",
                                    style={"whiteSpace": "nowrap", "fontSize": "0.7rem"}
                                ),
                            ]
                        ),
                    ],
                    className="mb-4"
                )
            ),

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
                                html.H4(
                                    "0",
                                    id="kpi-avg-loc",
                                    className="text-center mb-1",
                                    style={"whiteSpace": "nowrap"}
                                ),
                                html.Small(
                                    "Min=0 | Max=0",
                                    id="kpi-avg-loc-subtext",
                                    className="text-center text-muted d-block",
                                    style={"whiteSpace": "nowrap", "fontSize": "0.7rem"}
                                ),
                            ]
                        ),
                    ],
                    className="mb-4"
                )
            ),

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
                                html.H4(
                                    "2.1",  # Example value; updated via callback
                                    id="kpi-avg-ccn",
                                    className="text-center mb-1",
                                    style={"whiteSpace": "nowrap"}
                                ),
                                html.Small(
                                    "Fn=768.3K | Total CCN=1.3M",
                                    id="kpi-ccn-subtext",
                                    className="text-center text-muted d-block",
                                    style={"whiteSpace": "nowrap", "fontSize": "0.7rem"}
                                ),
                            ]
                        ),
                    ],
                    className="mb-4"
                )
            ),

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
                                html.H4(
                                    "0",
                                    id="kpi-avg-repo-size",
                                    className="text-center mb-1",
                                    style={"whiteSpace": "nowrap"}
                                ),
                                html.Small(
                                    "Min=0 | Max=0",
                                    id="kpi-avg-repo-size-subtext",
                                    className="text-center text-muted d-block",
                                    style={"whiteSpace": "nowrap", "fontSize": "0.7rem"}
                                ),
                            ]
                        ),
                    ],
                    className="mb-4"
                )
            ),
        ],
        className="mb-4 mt-4",
        justify="around"
    )
