"""
Tool: volunteer_registry_api
Wraps the volunteer registry data source.
Replace the stub methods with real API/DB calls for your environment.
"""

from typing import Any


def search_volunteers(
    required_skills: list[str],
    available_on: str,          # ISO 8601 date string
    location: str,
    min_reliability_score: float = 0.0,
    max_results: int = 10,
) -> dict[str, Any]:
    """
    Return a ranked list of volunteers matching the given criteria.

    Returns:
        {
            "candidates": [
                {"volunteer_id": str, "match_score": float, "skills": [...], ...},
                ...
            ]
        }
    """
    raise NotImplementedError("Replace with real registry query")


def get_volunteer(volunteer_id: str) -> dict[str, Any]:
    """
    Return full profile for a single volunteer.

    Returns:
        {
            "volunteer_id": str,
            "name": str,
            "email": str,
            "phone": str,
            "preferred_channel": "email" | "sms" | "push",
            "skills": [...],
            "reliability_score": float,
        }
    """
    raise NotImplementedError("Replace with real registry query")


def update_volunteer_history(
    volunteer_id: str,
    project_id: str,
    outcome: str,               # "completed" | "no_show" | "cancelled"
) -> dict[str, Any]:
    """
    Record a volunteer's participation outcome for a project.

    Returns:
        {"success": bool}
    """
    raise NotImplementedError("Replace with real registry write")
