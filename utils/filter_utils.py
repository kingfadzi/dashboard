from dash import Input, State

FILTER_KEYS = [
    "host_name",
    "app_id",
    "transaction_cycle",
    "main_language",
    "classification_label",
    "activity_status",
]

# Use shared dcc.Store for filters
FILTER_INPUTS = [Input("default-filter-store", "data")]
FILTER_STATES = [State("default-filter-store", "data")]

def extract_filter_dict(data):
    return data or {}

def extract_filter_dict_from_store(store_data):
    if store_data is None:
        store_data = {}
    return {k: store_data.get(k) for k in FILTER_KEYS}


