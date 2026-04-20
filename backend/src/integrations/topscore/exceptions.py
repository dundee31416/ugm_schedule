"""Custom exceptions for the TopScore API client."""


class TopScoreError(Exception):
    """Base exception for all TopScore client errors."""


class TopScoreAuthError(TopScoreError):
    """Raised when authentication fails (401) or token retrieval fails."""


class TopScoreNotFoundError(TopScoreError):
    """Raised when a requested resource is not found (404)."""


class TopScoreRateLimitError(TopScoreError):
    """Raised when the API rate limit is exceeded (429)."""


class TopScoreAPIError(TopScoreError):
    """Raised for any other API-level error (4xx / 5xx)."""
