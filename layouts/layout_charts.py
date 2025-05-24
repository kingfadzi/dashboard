from dash import dcc, html
import dash_bootstrap_components as dbc

def chart_layout(filters=None):
    return dbc.Container([

        # Row: Repo Status & Classification
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(html.B("Repo Status", className="text-center"), className="bg-light"),
                    dcc.Graph(id="active-inactive-bar", config={"displayModeBar": False}, style={"height": 300}),
                ], className="mb-4"),
                width=6,
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(html.B("Repository Sizes", className="text-center"), className="bg-light"),
                    dcc.Graph(id="classification-pie", config={"displayModeBar": False}, style={"height": 300}),
                ], className="mb-4"),
                width=6,
            )
        ]),

        # Code Contribution Activity
        dbc.Card([
            dbc.CardHeader(html.B("Code Contribution Activity", className="text-center"), className="bg-light"),
            dcc.Graph(id="scatter-plot", config={"displayModeBar": False}, style={"height": 300}),
        ], className="mb-4"),

        # Multilingual Primary Language
        dbc.Card([
            dbc.CardHeader(html.B("Primary Language in Multilingual Repos", className="text-center"), className="bg-light"),
            dcc.Graph(id="repos-by-language-bar", config={"displayModeBar": False}, style={"height": 300}),
        ], className="mb-4"),

        # Row: Language Buckets & Last Commit
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(html.B("Num of Languages Used per Repo", className="text-center"), className="bg-light"),
                    dcc.Graph(id="language-usage-buckets-bar", config={"displayModeBar": False}, style={"height": 300}),
                ], className="mb-4"),
                width=6,
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(html.B("Last Commit Date", className="text-center"), className="bg-light"),
                    dcc.Graph(id="last-commit-buckets-bar", config={"displayModeBar": False}, style={"height": 300}),
                ], className="mb-4"),
                width=6,
            ),
        ]),

        # CLOC
        dbc.Card([
            dbc.CardHeader(html.B("Total Lines of Code", className="text-center"), className="bg-light"),
            dcc.Graph(id="cloc-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
        ], className="mb-4"),

        # IaC
        dbc.Card([
            dbc.CardHeader(html.B("Infrastructure as Code Usage", className="text-center"), className="bg-light"),
            dcc.Graph(id="iac-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
        ], className="mb-4", id="iac-card"),

        # Heatmap: Language vs Contributors
        dbc.Card([
            dbc.CardHeader(html.B("Code Contribution by Language", className="text-center"), className="bg-light"),
            dcc.Graph(id="language-contributors-heatmap", config={"displayModeBar": False}, style={"height": 600}),
        ], className="mb-4"),

        # Row: Trivy and Semgrep
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(html.B("Vulnerabilities by Severity (Shallow scan)", className="text-center"), className="bg-light"),
                    dcc.Graph(id="trivy-vulnerabilities-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
                ], className="mb-4"),
                width=6,
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(html.B("Standards Issues", className="text-center"), className="bg-light"),
                    dcc.Graph(id="semgrep-findings-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
                ], className="mb-4"),
                width=6,
            ),
        ]),

        # Application Server Usage
        dbc.Card([
            dbc.CardHeader(html.B("Application Server Usage", className="text-center"), className="bg-light"),
            dcc.Graph(id="appserver-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
        ], className="mb-4", id="appserver-card"),

        # Developer Frameworks
        dbc.Card([
            dbc.CardHeader(html.B("Top Developer Frameworks", className="text-center"), className="bg-light"),
            dcc.Graph(id="dev-frameworks-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
        ], className="mb-4", id="dev-frameworks-card"),

        # Package Type Distribution
        html.Div(
            id="package-type-card-container",
            children=[
                dbc.Card([
                    dbc.CardHeader(html.B("Package Type Distribution", className="text-center"), className="bg-light"),
                    dcc.Graph(id="package-type-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
                ], className="mb-4", id="package-type-card")
            ]
        ),


        # Optional dynamic chart section
        html.Div(id="label-tech-layout"),
    ], fluid=True)
