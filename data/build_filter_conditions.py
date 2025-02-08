def build_filter_conditions(filters, alias=None):
    """
    Builds SQL WHERE conditions from filter parameters.
    
    - Handles **free-text** searches (e.g., `app_id` using `ILIKE '%value%'`).
    - Handles **list-based** filters (e.g., `status IN ('active', 'inactive')`).
    - Supports **table aliasing** (for JOIN queries).
    
    Returns:
        condition_string (str): The SQL WHERE clause.
        param_dict (dict): Query parameters.
    """

    if not filters:
        return None, {}

    text_search_fields = {"app_id", "all_languages", "name"}  # Fields that use wildcards
    conditions = []
    param_dict = {}
    placeholder_counter = 1

    for field, values in filters.items():
        if not values:
            continue

        col = f"{alias}.{field}" if alias else field

        # Ensure values are always a list (even if a single string is passed)
        values = values if isinstance(values, list) else [values]

        if field in text_search_fields:
            or_clauses = []
            for val in values:
                placeholder = f"p{placeholder_counter}"
                placeholder_counter += 1
                param_dict[placeholder] = f"%{val}%"  # Partial match with wildcards
                or_clauses.append(f"{col} ILIKE :{placeholder}")  # Case-insensitive search
            if or_clauses:
                conditions.append("(" + " OR ".join(or_clauses) + ")")
        else:
            # List-based filters (e.g., status IN ('active', 'inactive'))
            placeholders = []
            for val in values:
                placeholder = f"p{placeholder_counter}"
                placeholder_counter += 1
                param_dict[placeholder] = val
                placeholders.append(f":{placeholder}")
            if placeholders:
                conditions.append(f"{col} IN ({', '.join(placeholders)})")

    if not conditions:
        return None, {}

    condition_string = " AND ".join(conditions)

    # 🔍 Debugging
    print("\n🔍 DEBUG: Final SQL WHERE Clause:", condition_string)
    print("🔍 DEBUG: SQL Parameters:", param_dict)

    return condition_string, param_dict