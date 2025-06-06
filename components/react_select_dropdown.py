from dash_extensions.enrich import DashProxy, ReactComponent
from dash import html

# Reference to react-select from unpkg
ReactSelect = ReactComponent(
    source="https://unpkg.com/react-select@5.7.3/dist/react-select.min.js",
    module="default",
    id="react-select"
)

def render_language_filter():
    return html.Div([
        # Hidden value store: the "real" selection
        html.Div(id="language-filter-real-container", children=[
            ReactSelect(
                id="language-filter-real",
                multi=True,
                placeholder="Select Language(s)",
                styles={
                    "menu": {"zIndex": 9999},
                    "valueContainer": {"maxHeight": "60px", "overflowY": "auto"},
                },
                # Options will be populated dynamically by callback
                options=[],
                value=[]
            )
        ]),
        # Proxy dcc.Dropdown to work with rest of app (real value gets copied here)
        html.Div([
            html.Div(
                id="language-filter-wrapper",
                style={"display": "none"},  # keep hidden but Dash needs it
                children=[
                    html.Div(id="language-filter", **{
                        "data-dash-is-loading": "true"
                    })
                ]
            )
        ])
    ])