"""
Tool: calendar_api
Creates and manages calendar events for community projects.
Replace the stub methods with real calendar integration for your environment.
"""

from typing import Any


def create_event(
    title: str,
    date: str,                  # ISO 8601
    location: str,
    attendee_ids: list[str],
    description: str = "",
) -> dict[str, Any]:
    """
    Create a calendar event and invite attendees.

    Returns:
        {
            "event_id": str,
            "created": bool,
            "conflicts_detected": [...],  # attendee_ids with existing conflicts
        }
    """
    raise NotImplementedError("Replace with real calendar integration")


def update_event(
    event_id: str,
    updates: dict,              # fields to update: date, location, attendees, etc.
) -> dict[str, Any]:
    """
    Update an existing calendar event.

    Returns:
        {"success": bool}
    """
    raise NotImplementedError("Replace with real calendar integration")


def cancel_event(event_id: str) -> dict[str, Any]:
    """
    Cancel a calendar event and notify attendees.

    Returns:
        {"success": bool}
    """
    raise NotImplementedError("Replace with real calendar integration")
