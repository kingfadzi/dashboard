from data.build_filter_conditions import build_filter_conditions

# Shared field → alias mapping
REPO_FILTER_FIELD_ALIAS_MAP = {
    "app_id": "hr",
    "tc": "hr",
    "main_language": "hr",
    "all_languages": "hr",
    "component_id": "hr",
    "repo_age_days": "rm",
    "number_of_contributors": "rm",
    "total_commits": "rm",
    "repo_size_bytes": "rm",
    "file_count": "rm",
    "total_lines_of_code": "rm",
    "name": "hr",
    "repo_slug": "hr",
    "activity_status": "hr",
    "browser_url": "hr",
    "classification_label": "hr",
}

def build_repo_filter_conditions(filters):
    return build_filter_conditions(filters, field_alias_map=REPO_FILTER_FIELD_ALIAS_MAP)

def normalize_version_sql(column_expr: str) -> str:
    return f"""
    CASE
      -- If it starts with digits-dot-digits, capture "major.minor" only:
      WHEN {column_expr} ~ '^[0-9]+\\.[0-9]+' 
        THEN regexp_replace({column_expr}, '^([0-9]+\\.[0-9]+).*$', '\\1')
      -- Otherwise if it starts with just digits (e.g. "1" or "2rc"), append ".0"
      WHEN {column_expr} ~ '^[0-9]+' 
        THEN regexp_replace({column_expr}, '^([0-9]+).*$', '\\1') || '.0'
      ELSE
        'Unknown'
    END
    """

