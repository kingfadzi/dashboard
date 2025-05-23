def build_filter_conditions(filters, alias=None, field_alias_map=None):
    if not filters:
        return None, {}

    text_search_fields = {"app_id", "all_languages", "name"}
    conditions = []
    param_dict = {}
    placeholder_counter = 1

    for field, values in filters.items():
        if not values:
            continue

        # Dynamically assign table alias per field
        if field_alias_map and field in field_alias_map:
            col = f"{field_alias_map[field]}.{field}"
        elif alias:
            col = f"{alias}.{field}"
        else:
            col = field

        values = values if isinstance(values, list) else [values]

        if field == "app_id":
            or_clauses = []
            repo_slug_col = f"{field_alias_map.get('repo_slug', alias)}.repo_slug" if field_alias_map else "repo_slug"
            for val in values:
                placeholder = f"p{placeholder_counter}"
                placeholder_counter += 1
                param_dict[placeholder] = f"%{val}%"
                or_clauses.append(f"({col} ILIKE :{placeholder} OR {repo_slug_col} ILIKE :{placeholder})")
            if or_clauses:
                conditions.append("(" + " OR ".join(or_clauses) + ")")

        elif field in text_search_fields:
            or_clauses = []
            for val in values:
                placeholder = f"p{placeholder_counter}"
                placeholder_counter += 1
                param_dict[placeholder] = f"%{val}%"
                or_clauses.append(f"{col} ILIKE :{placeholder}")
            if or_clauses:
                conditions.append("(" + " OR ".join(or_clauses) + ")")

        else:
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

    print("\nDEBUG: Final SQL WHERE Clause:", condition_string)
    print("DEBUG: SQL Parameters:", param_dict)

    return condition_string, param_dict
