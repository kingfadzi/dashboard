import uuid

def build_modal_store_payload(chart_id, field, click_data):
    print(f"[BUILD PAYLOAD] chart_id = {chart_id}")
    print(f"[BUILD PAYLOAD] field = {field}")
    print(f"[BUILD PAYLOAD] raw click_data = {click_data}")

    if not click_data or "points" not in click_data:
        print("[BUILD PAYLOAD] Invalid or missing click_data.")
        return None

    try:
        value = click_data["points"][0]["x"]
        payload = {
            "chart_id": chart_id,
            "click_data": {field: value},
            "uid": str(uuid.uuid4()),
        }
        print(f"[BUILD PAYLOAD] constructed payload = {payload}")
        return payload
    except (KeyError, IndexError, TypeError) as e:
        print(f"[BUILD PAYLOAD] Error extracting value: {e}")
        return None
