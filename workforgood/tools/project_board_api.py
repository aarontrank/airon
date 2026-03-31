"""
Tool: project_board_api
Wraps the community project data source.
Replace the stub methods with real API/DB calls for your environment.
"""

from typing import Any


def get_project(project_id: str) -> dict[str, Any]:
    """
    Return full details for a community project.

    Returns:
        {
            "project_id": str,
            "title": str,
            "description": str,
            "date": str,            # ISO 8601
            "location": str,
            "required_skills": [...],
            "required_headcount": int,
            "roles_needed": [...],
            "priority": "standard" | "high" | "critical",
            "status": "open" | "filled" | "completed" | "cancelled",
        }
    """
    raise NotImplementedError("Replace with real project board query")


def list_open_projects() -> dict[str, Any]:
    """
    Return all projects with status == 'open'.

    Returns:
        {"projects": [...]}
    """
    raise NotImplementedError("Replace with real project board query")


def update_project_status(
    project_id: str,
    status: str,                # "open" | "filled" | "completed" | "cancelled"
) -> dict[str, Any]:
    """
    Update the status of a project.

    Returns:
        {"success": bool}
    """
    raise NotImplementedError("Replace with real project board write")
