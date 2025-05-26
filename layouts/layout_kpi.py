import dash_bootstrap_components as dbc
from dash import html

def kpi_layout():
    return dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Total Repos", className="text-center bg-light",
                                       style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}),
                        dbc.CardBody([
                            html.H4("0", id="kpi-total-repos", className="text-center", style={"whiteSpace": "nowrap"}),
                            html.Small("Total=0", id="kpi-total-repos-subtext",
                                       className="text-center text-muted d-block",
                                       style={"whiteSpace": "nowrap", "fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4"
                )
            ),

            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Commits (Median)", className="text-center bg-light",
                                       style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}),
                        dbc.CardBody([
                            html.H4("0", id="kpi-avg-commits", className="text-center mb-1",
                                    style={"whiteSpace": "nowrap"}),
                            html.Small("IQR=0 | Outliers=0", id="kpi-avg-commits-subtext",
                                       className="text-center text-muted d-block",
                                       style={"whiteSpace": "nowrap", "fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4"
                )
            ),

            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Contributors (Median)", className="text-center bg-light",
                                       style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}),
                        dbc.CardBody([
                            html.H4("0", id="kpi-avg-contributors", className="text-center mb-1",
                                    style={"whiteSpace": "nowrap"}),
                            html.Small("IQR=0 | Outliers=0", id="kpi-avg-contributors-subtext",
                                       className="text-center text-muted d-block",
                                       style={"whiteSpace": "nowrap", "fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4"
                )
            ),

            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Lines of Code (Median)", className="text-center bg-light",
                                       style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}),
                        dbc.CardBody([
                            html.H4("0", id="kpi-avg-loc", className="text-center mb-1",
                                    style={"whiteSpace": "nowrap"}),
                            html.Small("IQR=0 | Outliers=0", id="kpi-avg-loc-subtext",
                                       className="text-center text-muted d-block",
                                       style={"whiteSpace": "nowrap", "fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4"
                )
            ),

            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Avg CCN", className="text-center bg-light",
                                       style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}),
                        dbc.CardBody([
                            html.H4("0.0", id="kpi-avg-ccn", className="text-center mb-1",
                                    style={"whiteSpace": "nowrap"}),
                            html.Small("Fn=0 | Total CCN=0", id="kpi-ccn-subtext",
                                       className="text-center text-muted d-block",
                                       style={"whiteSpace": "nowrap", "fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4"
                )
            ),

            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Repo Size (Median)", className="text-center bg-light",
                                       style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}),
                        dbc.CardBody([
                            html.H4("0", id="kpi-avg-repo-size", className="text-center mb-1",
                                    style={"whiteSpace": "nowrap"}),
                            html.Small("IQR=0 | Outliers=0", id="kpi-avg-repo-size-subtext",
                                       className="text-center text-muted d-block",
                                       style={"whiteSpace": "nowrap", "fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4"
                )
            ),

            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Branches (Median)", className="text-center bg-light",
                                       style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}),
                        dbc.CardBody([
                            html.H4("0", id="kpi-branches", className="text-center mb-1",
                                    style={"whiteSpace": "nowrap"}),
                            html.Small("IQR=0 | Outliers=0", id="kpi-branches-subtext",
                                       className="text-center text-muted d-block",
                                       style={"whiteSpace": "nowrap", "fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4"
                )
            ),

            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Repo Age (Days)", className="text-center bg-light",
                                       style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}),
                        dbc.CardBody([
                            html.H4("0", id="kpi-repo-age", className="text-center mb-1",
                                    style={"whiteSpace": "nowrap"}),
                            html.Small("IQR=0 | Outliers=0", id="kpi-repo-age-subtext",
                                       className="text-center text-muted d-block",
                                       style={"whiteSpace": "nowrap", "fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4"
                )
            ),
        ],
        className="mb-4 mt-4",
        justify="around"
    )
