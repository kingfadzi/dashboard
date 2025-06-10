from dash import html
import dash_bootstrap_components as dbc
from layouts.layout_charts import chart_layout
from layouts.layout_kpi import kpi_layout

def main_layout():
    return dbc.Container(
        [
            # Hidden div for potential layout information.
            html.Div(id="app-layout", style={"display": "none"}),

            # Main title.
            html.H1(
                "Custom Dashboard",
                className="bg-secondary text-white p-2 mb-4 text-center"
            ),

            # KPI Cards layout.
            kpi_layout(),

            # Row containing the filters on the left and the charts on the right.
            dbc.Row(
                [

                    dbc.Col(chart_layout(), md=9),
                ]
            ),
        ],
        fluid=True,
    )
