from dash import Input, Output
from urllib.parse import urlencode

def sanitize(value):
    if isinstance(value, list):
        return value[0] if value else None
    return value

def register_switch_view_callbacks(app):
    @app.callback(
        Output("switch-to-table-link", "href"),
        Input("host-name-filter", "value"),
        Input("activity-status-filter", "value"),
        Input("tc-filter", "value"),
        Input("language-filter", "value"),
        Input("classification-filter", "value"),
    )
    def build_table_link(host, status, tc, language, classification):
        query = {}
        if sanitize(host): query["host_name"] = sanitize(host)
        if sanitize(status): query["activity_status"] = sanitize(status)
        if sanitize(tc): query["transaction_cycle"] = sanitize(tc)
        if sanitize(language): query["main_language"] = sanitize(language)
        if sanitize(classification): query["classification_label"] = sanitize(classification)
        return "/table?" + urlencode(query) if query else "/table"

    @app.callback(
        Output("switch-to-graphs-link", "href"),
        Input("host-name-filter", "value"),
        Input("activity-status-filter", "value"),
        Input("tc-filter", "value"),
        Input("language-filter", "value"),
        Input("classification-filter", "value"),
    )
    def build_graphs_link(host, status, tc, language, classification):
        query = {}
        if sanitize(host): query["host_name"] = sanitize(host)
        if sanitize(status): query["activity_status"] = sanitize(status)
        if sanitize(tc): query["transaction_cycle"] = sanitize(tc)
        if sanitize(language): query["main_language"] = sanitize(language)
        if sanitize(classification): query["classification_label"] = sanitize(classification)
        return "/graphs?" + urlencode(query) if query else "/graphs"
