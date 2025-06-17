import pandas as pd
import json
from datetime import timezone
from zoneinfo import ZoneInfo
from dash import html
import dash_bootstrap_components as dbc


def render(log_df: pd.DataFrame) -> html.Div:

    if log_df is None or log_df.empty:
        return dbc.Card(
            dbc.CardBody(
                html.Small("No analysis log available.", className="text-muted")
            ),
            className="mb-4 shadow-sm",
        )

    header = html.Thead(html.Tr([
        html.Th("Executed At"),
        html.Th("Stage"),
        html.Th("Status"),
        html.Th("Duration (s)"),
        html.Th("Run ID"),
        html.Th("Result"),
    ]))

    def format_result(msg: str) -> html.Div:
        if not msg:
            display_text = "-"
        else:
            try:
                parsed = json.loads(msg)
                display_text = json.dumps(parsed, indent=2)
            except Exception:
                display_text = msg
        return html.Div(
            html.Pre(display_text, style={
                "margin": 0,
                "whiteSpace": "pre-wrap"
            }),
            style={
                "maxHeight": "200px",
                "overflowY": "auto",
                "padding": "4px",
                "fontSize": "0.85rem"
            }
        )

    body = html.Tbody([
        html.Tr([
            html.Td(
                row.execution_time.replace(tzinfo=timezone.utc)
                .astimezone(ZoneInfo("America/New_York"))
                .strftime("%B %d, %Y %I:%M %p"),
                style={"whiteSpace": "nowrap"}
            ),
            html.Td(row.stage or "-", style={"whiteSpace": "nowrap"}),
            html.Td(
                row.status,
                style={
                    "whiteSpace": "nowrap",
                    **({"color": "red"} if row.status == "FAILURE" else {})
                }
            ),
            html.Td(f"{row.duration:.2f}", style={"whiteSpace": "nowrap"}),
            html.Td(row.run_id or "-", style={"whiteSpace": "nowrap"}),
            html.Td(
                format_result(getattr(row, 'message', None) or ""),
                style={"whiteSpace": "normal"}
            ),
        ])
        for row in log_df.itertuples()
    ])

    table = dbc.Table(
        [header, body],
        bordered=True,
        hover=True,
        size="sm",
        responsive=True,
        className="small",
    )

    return dbc.Card(
        dbc.CardBody([
            html.H4('Last Analysis Log', className='card-title mb-3'),
            html.Div(
                table,
                style={
                    "padding": "1rem",
                    "borderLeft": "4px solid #f7dc6f",
                    "backgroundColor": "#fef9e7",
                    "borderRadius": "6px",
                }
            )
        ]),
        className="mb-4 shadow-sm"
    )
