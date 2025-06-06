from dash_extensions import ReactSelect
from dash import html


def render_language_filter():
    return html.Div([
        # This is the visible, scrollable filter
        ReactSelect(
            id="language-filter-real",
            isMulti=True,
            placeholder="Select Language(s)",
            styles={
                "menu": {"zIndex": 9999},
                "valueContainer": {"maxHeight": "60px", "overflowY": "auto"},
            },
            options=[],
            value=[]
        ),
        # Hidden Dash component for persistence and callbacks
        html.Div(
            id="language-filter",
            style={"display": "none"}
        )
    ])