"""
Memory Interface
Agents read and write memory through this module only.
Swap the backend (file, database, RAG) here without touching agent code.
"""

import json
from pathlib import Path
from typing import Any

CONTEXT_DIR = Path(__file__).parent / "context"

# Registry maps memory source names (used in agent definitions) to file paths.
MEMORY_REGISTRY: dict[str, Path] = {
    "volunteer_history": CONTEXT_DIR / "volunteer_history.json",
    "project_outcomes": CONTEXT_DIR / "project_outcomes.json",
    "no_show_log": CONTEXT_DIR / "no_show_log.json",
}


def read(source: str) -> Any:
    """
    Read from a named memory source.

    Args:
        source: Key from MEMORY_REGISTRY (e.g., "volunteer_history")

    Returns:
        Parsed JSON content of the memory file.

    Raises:
        KeyError: If source is not registered.
        FileNotFoundError: If the memory file does not exist.
    """
    path = _resolve(source)
    with open(path) as f:
        return json.load(f)


def write(source: str, data: Any) -> None:
    """
    Overwrite a named memory source with new data.

    Args:
        source: Key from MEMORY_REGISTRY
        data: JSON-serializable content to write

    Raises:
        KeyError: If source is not registered.
    """
    path = _resolve(source)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def append(source: str, record: dict) -> None:
    """
    Append a single record to a list-based memory source.

    Args:
        source: Key from MEMORY_REGISTRY
        record: Dict to append

    Raises:
        KeyError: If source is not registered.
        ValueError: If existing content is not a list.
    """
    existing = read(source)
    if not isinstance(existing, list):
        raise ValueError(f"Memory source '{source}' does not contain a list")
    existing.append(record)
    write(source, existing)


def _resolve(source: str) -> Path:
    if source not in MEMORY_REGISTRY:
        raise KeyError(f"Unknown memory source: '{source}'. Register it in MEMORY_REGISTRY.")
    return MEMORY_REGISTRY[source]


# --- Future backend swap point ---
# To switch to a database or RAG system, replace the read/write/append
# implementations above. The interface (function signatures and return types)
# must remain identical so agents require no changes.
