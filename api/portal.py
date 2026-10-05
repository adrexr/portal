"""JSON adapters for the demo results portal."""

from care_portal.records import acknowledge_follow_up, portal_payload


def access_portal_payload(data: dict) -> dict:
    return {"success": True, "data": portal_payload(str(data.get("access_code", "")))}


def acknowledge_payload(data: dict) -> dict:
    return acknowledge_follow_up(str(data.get("access_code", "")), str(data.get("record_id", "")))
