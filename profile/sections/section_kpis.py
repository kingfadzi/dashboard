from dash import html
import dash_bootstrap_components as dbc

def render(profile_data):
    return dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Repo Size", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(f"{profile_data['Repo Size (MB)']} MB", className="text-center"),
                            html.Small(f"Files={profile_data['File Count']}", className="text-center text-muted d-block", style={"fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4 shadow-sm"
                ),
                xs=12, sm=6, md=4, lg=2
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Lines of Code", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(f"{profile_data['Lines of Code']:,}", className="text-center"),
                            html.Small("All files", className="text-center text-muted d-block", style={"fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4 shadow-sm"
                ),
                xs=12, sm=6, md=4, lg=2
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Contributors", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(f"{profile_data['Contributors']}", className="text-center"),
                            html.Small("Active", className="text-center text-muted d-block", style={"fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4 shadow-sm"
                ),
                xs=12, sm=6, md=4, lg=2
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Active Branches", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(f"{profile_data['Active Branch Count']}", className="text-center"),
                            html.Small("Main + Dev", className="text-center text-muted d-block", style={"fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4 shadow-sm"
                ),
                xs=12, sm=6, md=4, lg=2
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Repo Age", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(f"{profile_data['Repo Age (Years)']} yrs", className="text-center"),
                            html.Small(f"Since {profile_data['Last Commit Date'][:4]}", className="text-center text-muted d-block", style={"fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4 shadow-sm"
                ),
                xs=12, sm=6, md=4, lg=2
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Activity Status", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(profile_data['Activity Status'], className="text-center"),
                            html.Small("Based on commits", className="text-center text-muted d-block", style={"fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4 shadow-sm"
                ),
                xs=12, sm=6, md=4, lg=2
            ),
        ],
        className="g-3 mb-4",
        justify="around"
    )