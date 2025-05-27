# config/config.py
import os
from dotenv import dotenv_values

def _load_default_filters():
    env_file = os.getenv("ENV_FILE", ".env")
    cfg = dotenv_values(env_file)

    def parse(v):
        return [x.strip() for x in v.split(",") if x.strip()] if v else []

    return {
        "host_name":         parse(cfg.get("DEFAULT_HOST_NAME")),
        "activity_status":   parse(cfg.get("DEFAULT_ACTIVITY_STATUS")),
        "transaction_cycle": parse(cfg.get("DEFAULT_TRANSACTION_CYCLE")),
        "main_language":     parse(cfg.get("DEFAULT_LANGUAGE")),
        "classification_label": parse(cfg.get("DEFAULT_CLASSIFICATION")),
        "app_id":            cfg.get("DEFAULT_APP_ID", ""),
    }

# Exported for imports
DEFAULT_FILTERS = _load_default_filters()
