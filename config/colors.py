import plotly.express as px
from dash import dcc
from plotly.graph_objs import Figure

DEFAULT_COLOR_SEQUENCE = px.colors.qualitative.Safe

def with_safe_colors(chart_func):
    def wrapper(*args, **kwargs):
        result = chart_func(*args, **kwargs)

        if isinstance(result, Figure):
            # chart function returned a raw Plotly figure
            fig = result
            graph_id = None
            config = {}
        elif isinstance(result, dcc.Graph):
            # chart function returned a dcc.Graph
            fig = result.figure
            graph_id = result.id
            config = result.config if hasattr(result, "config") else {}
        else:
            raise TypeError("Expected chart function to return a plotly Figure or dcc.Graph")

        # Apply default colorway only if none set
        if not fig.layout.get("colorway"):
            fig.update_layout(colorway=DEFAULT_COLOR_SEQUENCE)

        return dcc.Graph(id=graph_id, figure=fig, config=config)
    return wrapper