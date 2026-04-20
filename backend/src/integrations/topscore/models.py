"""Simple data-classes for wrapping TopScore API responses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TopScoreResponse:
    """
    Wrapper around a raw TopScore API response.

    TopScore always returns JSON with four top-level keys::

        {
            "status": 200,
            "result": <list or object>,
            "count":  42,
            "errors": []
        }

    Attributes:
        status:  HTTP status code echoed by the API.
        result:  The actual payload (list or dict).
        count:   Number of items in ``result`` (convenience field).
        errors:  List of error strings (empty on success).
        raw:     The complete parsed JSON dictionary.
    """

    status: int
    result: Any
    count: Optional[int]
    errors: List[str]
    raw: Dict[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        """True when the status code is in the 2xx range."""
        return 200 <= self.status < 300

    def __repr__(self) -> str:
        count_info = f", count={self.count}" if self.count is not None else ""
        return f"TopScoreResponse(status={self.status}{count_info}, ok={self.ok})"
