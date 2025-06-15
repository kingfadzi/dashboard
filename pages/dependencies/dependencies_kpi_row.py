from dash import html


def kpi_stat(label, value_id):
    return html.Div(
        [
            html.Span(f"{label}:", className="text-muted small me-1"),
            html.Span("—", id=value_id, className="fw-semibold", style={"fontVariantNumeric": "tabular-nums"}),
        ],
        className="me-4 d-flex align-items-center"
    )


def dependencies_kpi_row():
    return html.Div(
        [
            kpi_stat("Repos", "dependencies_kpi-total-repos"),
            kpi_stat("Dependencies", "dependencies_kpi-total-deps"),
            kpi_stat("Repos with Deps", "dependencies_kpi-repos-with-deps"),
            kpi_stat("Repos without Deps", "dependencies_kpi-repos-without-deps"),
        ],
        className="d-flex flex-wrap align-items-center ms-3",
        style={"fontSize": "0.9rem"}
    )
