from dash import html


def kpi_stat(label, value_id):
    return html.Div(
        [
            html.Span(f"{label}:", className="text-muted small me-1"),
            html.Span("—", id=value_id, className="fw-semibold", style={"fontVariantNumeric": "tabular-nums"}),
        ],
        className="me-4 d-flex align-items-center"
    )


def build_tools_kpi_row():
    return html.Div(
        [
            kpi_stat("Repos", "build_tools_kpi-total-repos"),
            kpi_stat("Build Tools", "build_tools_kpi-total-variants"),
            kpi_stat("Runtime Versions", "build_tools_kpi-total-runtimes"),
            kpi_stat("No Tool Detected", "build_tools_kpi-no-tool"),
        ],
        className="d-flex flex-wrap align-items-center ms-3",
        style={"fontSize": "0.9rem"}
    )
