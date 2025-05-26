from dotenv import dotenv_values
import os

DEFAULT_FILTERS = {}

def load_default_filters():
    env_file = os.getenv("ENV_FILE", ".env")
    config = dotenv_values(env_file)

    def parse(val):
        if not val:
            return []
        return [v.strip() for v in val.split(",")]

    filters = {
        "host_name": parse(config.get("DEFAULT_HOST_NAME")),
        "activity_status": parse(config.get("DEFAULT_ACTIVITY_STATUS")),
        "transaction_cycle": parse(config.get("DEFAULT_TRANSACTION_CYCLE")),
        "language": parse(config.get("DEFAULT_LANGUAGE")),
        "classification": parse(config.get("DEFAULT_CLASSIFICATION")),
    }

    print("✅ Loaded DEFAULT_FILTERS from .env:", filters)
    return filters
