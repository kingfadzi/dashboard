from dash import html
import dash_bootstrap_components as dbc

def render(profile_data):
    activity_status = profile_data.get('Activity Status', 'Inactive')
    last_commit_date = profile_data.get('Last Commit Date', 'N/A')
    badge_color = "success" if activity_status.upper() == "ACTIVE" else "danger"

    return dbc.Row(
        [
            # --- Activity Status first ---
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Activity Status", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.Div(
                                dbc.Badge(activity_status, color=badge_color, className="p-2", style={"fontSize": "0.9rem"}),
                                className="text-center mb-2"
                            ),
                            html.Small(
                                f"Last commit: {last_commit_date.split('T')[0]}",
                                className="text-center text-muted d-block",
                                style={"fontSize": "0.7rem"}
                            )
                        ])
                    ],
                    className="mb-4 shadow-sm"
                ),
                xs=12, sm=6, md=4, lg=2
            ),

            # --- Repo Age ---
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Repo Age", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(f"{profile_data.get('Repo Age (Years)', 0)} yrs", className="text-center"),
                            html.Small(
                                f"Since {str(profile_data.get('Last Commit Date', 'N/A'))[:4]}",
                                className="text-center text-muted d-block",
                                style={"fontSize": "0.7rem"}
                            )
                        ])
                    ],
                    className="mb-4 shadow-sm"
                ),
                xs=12, sm=6, md=4, lg=2
            ),

            # --- Repo Size ---
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Repo Size", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(f"{profile_data.get('Repo Size (MB)', 0)} MB", className="text-center"),
                            html.Small(f"Code Size (MB)={profile_data.get('Code Size (MB)', 0)} MB", className="text-center text-muted d-block", style={"fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4 shadow-sm"
                ),
                xs=12, sm=6, md=4, lg=2
            ),

            # --- Lines of Code ---
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Lines of Code", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(f"{profile_data.get('Lines of Code', 0):,}", className="text-center"),
                            html.Small("All files", className="text-center text-muted d-block", style={"fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4 shadow-sm"
                ),
                xs=12, sm=6, md=4, lg=2
            ),

            # --- Contributors ---
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Contributors", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(f"{profile_data.get('Contributors', 0)}", className="text-center"),
                            html.Small("All time", className="text-center text-muted d-block", style={"fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4 shadow-sm"
                ),
                xs=12, sm=6, md=4, lg=2
            ),

            # --- Active Branches ---
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Active Branches", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(f"{profile_data.get('Active Branch Count', 0)}", className="text-center"),
                            html.Small("Main + Dev", className="text-center text-muted d-block", style={"fontSize": "0.7rem"})
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
