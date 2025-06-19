def human_readable_age(days):
    if days < 7:
        return f"{days} days"
    elif days < 30:
        return f"{days // 7} weeks"
    elif days < 365:
        return f"{days // 30} months"
    else:
        return f"{days // 365} years"

def human_readable_size(size_in_bytes):
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < 1024**2:
        return f"{size_in_bytes / 1024:.2f} KB"
    elif size_in_bytes < 1024**3:
        return f"{size_in_bytes / 1024**2:.2f} MB"
    elif size_in_bytes < 1024**4:
        return f"{size_in_bytes / 1024**3:.2f} GB"
    else:
        return f"{size_in_bytes / 1024**4:.2f} TB"

def human_readable_counts(value):
    if value is None:
        return "0"
    value = int(value)
    if value < 1_000:
        return f"{value}"
    elif value < 1_000_000:
        return f"{value / 1_000:.1f}K"
    elif value < 1_000_000_000:
        return f"{value / 1_000_000:.1f}M"
    else:
        return f"{value / 1_000_000_000:.1f}B"


def deduplicate_comma_separated_values(values):
    if not values:
        return ""
    unique_values = set(values.split(","))
    return ",".join(sorted(unique_values))