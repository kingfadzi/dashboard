from dash import html


def kpi_stat(label, value_id):
    return html.Div(
        [
            html.Span(f"{label}:", className="text-muted small me-1"),
            html.Span("—", id=value_id, className="fw-semibold", style={"fontVariantNumeric": "tabular-nums"}),
        ],
        className="me-4 d-flex align-items-center"
    )


def code_insights_kpi_row():
    return html.Div(
        [
            kpi_stat("Repos", "code_insights_kpi-total-repos"),
            kpi_stat("LOC", "code_insights_kpi-total-loc"),
            kpi_stat("Functions", "code_insights_kpi-total-functions"),
            kpi_stat("Files", "code_insights_kpi-total-files"),
        ],
        className="d-flex flex-wrap align-items-center ms-3",
        style={"fontSize": "0.9rem"}
    )
