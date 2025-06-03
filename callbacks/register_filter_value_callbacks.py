import json
from dash import Input, Output, State, callback, ctx
from dash.exceptions import PreventUpdate
import dash

def register_filter_value_callbacks(app):
    @callback(
        [
            Output("activity-status-filter", "value"),
            Output("tc-filter", "value"),
            Output("language-filter", "value"),
            Output("classification-filter", "value"),
            Output("app-id-filter", "value"),
            Output("host-name-filter", "value"),
            Output("default-filter-store", "data"),
        ],
        [
            Input("default-filter-store", "modified_timestamp"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
            Input("host-name-filter", "value"),
        ],
        [
            State("default-filter-store", "data"),
            State("activity-status-filter", "options"),
            State("tc-filter", "options"),
            State("language-filter", "options"),
            State("classification-filter", "options"),
            State("host-name-filter", "options"),
        ],
        prevent_initial_call=False,
    )
    def unified_filter_logic(mod_ts, activity, tc, lang, classification, app_id, host,
                         store_data,
                         activity_opts, tc_opts, lang_opts, class_opts, host_opts):
        print("\n[unified_filter_logic] Triggered by:", ctx.triggered_id)
        print(f"[unified_filter_logic] Store data: {json.dumps(store_data, indent=2)}")
    
        def validate(vals, options):
            valid = {o["value"] for o in options}
            return [v for v in vals if v in valid]
    
        # 1. Initialize store if empty
        if store_data is None:
            initial = {
                "host_name": [],
                "activity_status": [],
                "transaction_cycle": [],
                "main_language": [],
                "classification_label": [],
                "app_id": ""
            }
            print("[unified_filter_logic] Initializing store")
            return [
                initial["activity_status"],
                initial["transaction_cycle"],
                initial["main_language"],
                initial["classification_label"],
                initial["app_id"],
                initial["host_name"],
                initial
            ]
    
        # 2. Handle store load (hydrate UI)
        if ctx.triggered_id == "default-filter-store":
            hydrated = [
                validate(store_data.get("activity_status", []), activity_opts),
                validate(store_data.get("transaction_cycle", []), tc_opts),
                validate(store_data.get("main_language", []), lang_opts),
                validate(store_data.get("classification_label", []), class_opts),
                store_data.get("app_id", ""),
                validate(store_data.get("host_name", []), host_opts),
                dash.no_update  # Don't modify store
            ]
            print("[unified_filter_logic] Hydrated filters from store.")
            return hydrated
    
        # 3. Handle filter changes (update store)
        updated = {
            "host_name": host,
            "activity_status": activity,
            "transaction_cycle": tc,
            "main_language": lang,
            "classification_label": classification,
            "app_id": app_id,
        }
        print("[unified_filter_logic] Updating store with:", json.dumps(updated, indent=2))
        
        # Return current UI values + updated store
        return [activity, tc, lang, classification, app_id, host, updated]