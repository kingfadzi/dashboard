import plotly.express as px
from dash import dcc
from plotly.graph_objs import Figure

DEFAULT_COLOR_SEQUENCE = px.colors.qualitative.Safe

def with_safe_colors(chart_func):
    def wrapper(*args, **kwargs):
        result = chart_func(*args, **kwargs)

        # If already a dcc.Graph, apply color patch and return it directly
        if isinstance(result, dcc.Graph):
            fig = result.figure
            if not hasattr(fig.layout, "colorway") or not fig.layout.colorway:
                fig.update_layout(colorway=DEFAULT_COLOR_SEQUENCE)
            return result
            
        # If it's a raw Figure, wrap it
        elif isinstance(result, Figure):
            fig = result
            if not hasattr(fig.layout, "colorway") or not fig.layout.colorway:
                fig.update_layout(colorway=DEFAULT_COLOR_SEQUENCE)
            graph_id = f"{chart_func.__name__}-graph"
            return dcc.Graph(id=graph_id, figure=fig)

        else:
            raise TypeError("Chart function must return plotly Figure or dcc.Graph")

    return wrapper