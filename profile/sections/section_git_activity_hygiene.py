from dash import html
import dash_bootstrap_components as dbc

def render(profile_data):
    return dbc.Card(
        dbc.CardBody([
            html.H4('Repository Activity & Hygiene', className='card-title mb-4'),

            dbc.Row([
                # Single Developer Risk
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader("Single Developer Risk", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(f"{profile_data['Single Developer %']}%", 
                                className="text-center",
                                style={"color": "red" if profile_data['Single Developer %'] > 75 
                                       else "orange" if profile_data['Single Developer %'] > 50 
                                       else "green"}
                            ),
                            html.Small(
                                "High Risk" if profile_data['Single Developer %'] > 75 
                                else "Moderate" if profile_data['Single Developer %'] > 50 
                                else "Healthy",
                                className="text-muted d-block text-center mt-2",
                                style={"fontSize": "0.7rem"}
                            )
                        ])
                    ]),
                    width=3
                ),

                # Repository Bloat Risk
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader("Repository Bloat Risk", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(f"{profile_data['Repo Size per File (MB)']:.2f} MB", 
                                className="text-center",
                                style={"color": "green" if profile_data['Repo Size per File (MB)'] < 0.5 
                                       else "orange" if profile_data['Repo Size per File (MB)'] <= 1.0 
                                       else "red"}
                            ),
                            html.Small(
                                "Healthy" if profile_data['Repo Size per File (MB)'] < 0.5 
                                else "Moderate" if profile_data['Repo Size per File (MB)'] <= 1.0 
                                else "Bloated",
                                className="text-muted d-block text-center mt-2",
                                style={"fontSize": "0.7rem"}
                            )
                        ])
                    ]),
                    width=3
                ),

                # Healthy Code Evolution
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader("Healthy Code Evolution", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(f"{profile_data['Commits-to-Files Ratio']:.1f}", 
                                className="text-center",
                                style={"color": "green" if profile_data['Commits-to-Files Ratio'] > 1.0 
                                       else "orange" if profile_data['Commits-to-Files Ratio'] >= 0.5 
                                       else "red"}
                            ),
                            html.Small(
                                "Good Growth" if profile_data['Commits-to-Files Ratio'] > 1.0 
                                else "Moderate Growth" if profile_data['Commits-to-Files Ratio'] >= 0.5 
                                else "Poor Growth",
                                className="text-muted d-block text-center mt-2",
                                style={"fontSize": "0.7rem"}
                            )
                        ])
                    ]),
                    width=3
                ),

                # Dormant Repository Risk
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader("Dormant Repository Risk", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(f"{profile_data['Days Since Last Commit']} days", 
                                className="text-center",
                                style={"color": "green" if profile_data['Days Since Last Commit'] < 90 
                                       else "orange" if profile_data['Days Since Last Commit'] <= 180 
                                       else "red"}
                            ),
                            html.Small(
                                "Active" if profile_data['Days Since Last Commit'] < 90 
                                else "Becoming Stale" if profile_data['Days Since Last Commit'] <= 180 
                                else "Dormant",
                                className="text-muted d-block text-center mt-2",
                                style={"fontSize": "0.7rem"}
                            )
                        ])
                    ]),
                    width=3
                ),

            ], className="g-4")
        ]),
        className="mb-4 shadow-sm"
    )