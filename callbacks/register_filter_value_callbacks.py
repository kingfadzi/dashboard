import json
from dash import Input, Output, State, callback, ctx
from dash.exceptions import PreventUpdate
import dash
from dash import html, dcc

def register_filter_value_callbacks(app):
    # 1. Define store with initial data
    dcc.Store(
        id="default-filter-store",
        storage_type="local",
        data={  # Initial structure
            "host_name": [],
            "activity_status": [],
            "transaction_cycle": [],
            "main_language": [],
            "classification_label": [],
            "app_id": ""
        }
    )
    
    # 2. Single callback for filter persistence
    @app.callback(
        Output("default-filter-store", "data"),
        Input("activity-status-filter", "value"),
        Input("tc-filter", "value"),
        Input("language-filter", "value"),
        Input("classification-filter", "value"),
        Input("app-id-filter", "value"),
        Input("host-name-filter", "value"),
        State("default-filter-store", "data"),
    )
    def persist_filter_values(activity, tc, lang, classification, app_id, host, current_store):
        # Only update if any value actually changed
        if (activity != current_store["activity_status"] or
            tc != current_store["transaction_cycle"] or
            lang != current_store["main_language"] or
            classification != current_store["classification_label"] or
            app_id != current_store["app_id"] or
            host != current_store["host_name"]):
            
            new_store = {
                "host_name": host or [],
                "activity_status": activity or [],
                "transaction_cycle": tc or [],
                "main_language": lang or [],
                "classification_label": classification or [],
                "app_id": app_id or ""
            }
            return new_store
        
        raise PreventUpdate
    
    # 3. Hydration callback (runs once when page loads)
    @app.callback(
        [
            Output("activity-status-filter", "value"),
            Output("tc-filter", "value"),
            Output("language-filter", "value"),
            Output("classification-filter", "value"),
            Output("app-id-filter", "value"),
            Output("host-name-filter", "value"),
        ],
        Input("default-filter-store", "data"),
        prevent_initial_call=True
    )
    def hydrate_filters(store_data):
        return [
            store_data["activity_status"],
            store_data["transaction_cycle"],
            store_data["main_language"],
            store_data["classification_label"],
            store_data["app_id"],
            store_data["host_name"],
        ]