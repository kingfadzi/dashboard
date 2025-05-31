# config/colors.py
import plotly.express as px

DEFAULT_COLOR_SEQUENCE = px.colors.qualitative.Safe

def with_safe_colors(chart_func):
    def wrapper(*args, **kwargs):
        graph = chart_func(*args, **kwargs)
        fig = graph.figure

        # Only set default colorway if none is already set
        if "colorway" not in fig.layout or not fig.layout.colorway:
            fig.update_layout(colorway=DEFAULT_COLOR_SEQUENCE)

        return dcc.Graph(
            id=graph.id,
            figure=fig,
            config=graph.config if hasattr(graph, "config") else {}
        )
    return wrapper