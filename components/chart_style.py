from functools import wraps
from components.colors import NEUTRAL_COLOR_SEQUENCE

def standard_chart_style(func):
    """Decorator to apply consistent styling to Plotly charts"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        fig = func(*args, **kwargs)

        # Preserve existing axis settings
        xaxis_existing = fig.layout.xaxis.to_plotly_json() if fig.layout.xaxis else {}
        yaxis_existing = fig.layout.yaxis.to_plotly_json() if fig.layout.yaxis else {}

        xaxis_style = {
            "showline": True,
            "linewidth": 1,
            "mirror": True,
            "ticks": "outside",
            "ticklen": 6,
            "fixedrange": True,
            "showgrid": False,
            "zeroline": False,
            "title_standoff": 15,
            "showticklabels": xaxis_existing.get("showticklabels", False),
            "title": {
                "text": xaxis_existing.get("title", {}).get("text", None),
                "standoff": 15
            }
        }

        yaxis_style = {
            "showline": True,
            "linewidth": 1,
            "mirror": True,
            "ticks": "outside",
            "ticklen": 6,
            "fixedrange": False,
            "showgrid": True,
            "gridcolor": "#e5e5e5",
            "gridwidth": 1,
            "zeroline": False,
            "title_standoff": 15,
            "showticklabels": yaxis_existing.get("showticklabels", True),
            "title": {
                "text": yaxis_existing.get("title", {}).get("text", None),
                "standoff": 15
            }
        }

        fig.update_layout(
            font=dict(family='Arial', size=12),
            margin=dict(t=40, b=20, l=20, r=20),
            plot_bgcolor='white',
            xaxis=xaxis_style,
            yaxis=yaxis_style,
            colorway=NEUTRAL_COLOR_SEQUENCE,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1,
                title_text="",
                font_size=10
            ),
            hoverlabel=dict(
                bgcolor='white',
                font_size=12,
                bordercolor='#cccccc'
            ),
            dragmode=False,
            title=None
        )

        fig.update_traces(
            texttemplate='%{text:.0f}',
            textposition='outside',
            cliponaxis=False
        )

        return fig

    return wrapper

def status_chart_style(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        fig = func(*args, **kwargs)

        # Preserve any existing axis titles/tick settings
        xaxis_existing = fig.layout.xaxis.to_plotly_json() if fig.layout.xaxis else {}
        yaxis_existing = fig.layout.yaxis.to_plotly_json() if fig.layout.yaxis else {}

        xaxis_style = {
            "title": xaxis_existing.get("title", {}).get("text", None),
            "title_standoff": 15,
            "showline": True,
            "linewidth": 1,
            "mirror": True,
            "ticks": "outside",
            "ticklen": 6,
            "fixedrange": True,
            "showgrid": True,
            "gridcolor": "#e5e5e5",
            "gridwidth": 1,
            "zeroline": False,

        }

        yaxis_style = {
            "title": None,
            "title_standoff": 15,
            "showline": True,
            "linewidth": 1,
            "mirror": True,
            "ticks": "outside",
            "ticklen": 6,
            "fixedrange": True,
            "showgrid": True,
            "gridcolor": "#e5e5e5",
            "gridwidth": 1,
            "zeroline": False,
            "showticklabels": yaxis_existing.get("showticklabels", True),
        }

        fig.update_layout(
            font=dict(family="Arial", size=12),
            margin=dict(t=60, b=20, l=20, r=20),
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis=xaxis_style,
            yaxis=yaxis_style,
            colorway=NEUTRAL_COLOR_SEQUENCE,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.0,
                xanchor="right",
                x=1.0,
                title_text="",
                font_size=10
            ),
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                bordercolor="#cccccc"
            ),
            dragmode=False,
            title=None
        )

        return fig

    return wrapper