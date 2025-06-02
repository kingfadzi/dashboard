layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        header_with_button,

        dbc.Row(
            [
                dbc.Col(card("Dependency Detection Coverage", "dep-detection-chart"), width=4),
                dbc.Col(card("IaC Detection Coverage",        "iac-detection-chart"), width=4),
                dbc.Col(card("EOL Detection Coverage",        "xeol-detection-chart"), width=4),
            ]
        ),

        html.Hr(),

        dbc.Row(
            [
                dbc.Col(card("Package Type Distribution", "package-type-distribution-chart"), width=6),
                dbc.Col(card("Framework Distribution",     "framework-distribution-chart"), width=6),
            ]
        ),

        dbc.Row([dbc.Col(card("Top Packages", "top-packages-chart"), width=12)]),

        dbc.Row(
            [
                dbc.Col(card("Spring Core Version Usage", "spring-core-version-chart"), width=6),
                dbc.Col(card("Spring Boot Version Usage", "spring-boot-version-chart"), width=6),
            ]
        ),

        dbc.Row([dbc.Col(card("EOL Top Products", "xeol-top-products-chart"), width=12)]),

        dbc.Row(
            [
                dbc.Col(card("Dependency Volume", "dependency-volume-chart"), width=6),
                dbc.Col(card("EOL Exposure",      "xeol-exposure-chart"), width=6),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(card("IaC Framework Usage", "iac-framework-usage-chart"), width=6),
                dbc.Col(card("IaC Adoption",         "iac-adoption-chart"),         width=6),
            ]
        ),

        dbc.Row(
            [dbc.Col(card("Application Servers / Orchestration Frameworks", "iac-server-orchestration-chart"), width=12)],
        ),

        html.Hr(),

        dbc.Row(
            [
                dbc.Col(card("Outdated Library Usage",       "outdated-library-chart"), width=6),
                dbc.Col(card("Legacy Version Exposure",      "legacy-version-chart"), width=6),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(card("JUnit Version Usage",          "junit-version-chart"), width=6),
                dbc.Col(card("Dependency Count per Repo",    "dependency-count-chart"), width=6),
            ]
        ),

        dbc.Row(
            [dbc.Col(card("Multiple Frameworks per Repo",   "frameworks-per-repo-chart"), width=12)],
        ),

        modal_table(),
        dcc.Store(id="default-filter-store"),
        dcc.Store(id="filters-applied-trigger"),
    ],
    fluid=True,
    style={"marginTop": "0px", "paddingTop": "0px"},
)