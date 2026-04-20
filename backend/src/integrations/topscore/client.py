"""
TopScore API Client

Provides authenticated access to the TopScore REST API.
Supports both unauthenticated GET requests and authenticated POST requests via OAuth2.

API docs: https://aum.usetopscore.com/api/help
"""

from __future__ import annotations

import time
import logging
from typing import Any, Dict, Iterator, List, Optional
from urllib.parse import urljoin

import requests
from requests import Response

from .exceptions import (
    TopScoreAuthError,
    TopScoreNotFoundError,
    TopScoreAPIError,
    TopScoreRateLimitError,
)
from .models import TopScoreResponse

logger = logging.getLogger(__name__)


class TopScoreClient:
    """
    Client for the TopScore REST API.

    Authentication uses OAuth2 client-credentials flow.  The access token is
    fetched lazily on the first authenticated request and refreshed automatically
    when it expires.

    Args:
        base_url:      Your TopScore domain, e.g. ``"https://aum.usetopscore.com"``.
        client_id:     OAuth2 client ID (auth_token shown in the developer panel).
        client_secret: OAuth2 client secret.
        csrf_token:    Optional CSRF token required by some POST endpoints.
        timeout:       Default request timeout in seconds (default: 30).
        max_retries:   Number of times to retry transient failures (default: 3).
    """

    _TOKEN_PATH = "/api/oauth/server"

    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        csrf_token: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret
        self.csrf_token = csrf_token
        self.timeout = timeout
        self.max_retries = max_retries

        self._session = requests.Session()
        self._session.headers.update({"Accept": "application/json"})

        self._access_token: Optional[str] = None
        self._token_expiry: float = 0.0

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    def _is_token_valid(self) -> bool:
        return self._access_token is not None and time.time() < self._token_expiry

    def _fetch_token(self) -> None:
        """Obtain a new OAuth2 access token using client credentials."""
        url = self.base_url + self._TOKEN_PATH
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        try:
            resp = self._session.post(url, data=payload, timeout=self.timeout)
            resp.raise_for_status()
        except requests.HTTPError as exc:
            raise TopScoreAuthError(
                f"Failed to obtain access token: {exc.response.status_code} {exc.response.text}"
            ) from exc
        except requests.RequestException as exc:
            raise TopScoreAuthError(f"Token request failed: {exc}") from exc

        data = resp.json()
        self._access_token = data.get("access_token")
        expires_in = int(data.get("expires_in", 3600))
        # Refresh 60 seconds before real expiry to avoid edge cases
        self._token_expiry = time.time() + expires_in - 60
        logger.debug("Obtained new access token (expires in %s s)", expires_in)

    def _ensure_auth(self) -> str:
        if not self._is_token_valid():
            self._fetch_token()
        return self._access_token  # type: ignore[return-value]

    # ------------------------------------------------------------------
    # Core request machinery
    # ------------------------------------------------------------------

    def _build_url(self, endpoint: str) -> str:
        # Accept both "/api/events" and "events" style
        if not endpoint.startswith("/"):
            endpoint = f"/api/{endpoint}"
        return self.base_url + endpoint

    def _request(
        self,
        method: str,
        endpoint: str,
        authenticated: bool = False,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> TopScoreResponse:
        url = self._build_url(endpoint)
        headers: Dict[str, str] = {}

        if authenticated:
            token = self._ensure_auth()
            headers["Authorization"] = f"Bearer {token}"

        if self.csrf_token and method.upper() == "POST":
            headers["X-CSRF-Token"] = self.csrf_token

        last_exc: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                resp: Response = self._session.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                    data=data,
                    json=json,
                    timeout=self.timeout,
                )
                return self._handle_response(resp)
            except TopScoreRateLimitError as exc:
                wait = 2 ** attempt
                logger.warning("Rate limited – retrying in %s s (attempt %s)", wait, attempt)
                time.sleep(wait)
                last_exc = exc
            except (requests.ConnectionError, requests.Timeout) as exc:
                logger.warning("Network error on attempt %s: %s", attempt, exc)
                last_exc = exc
                time.sleep(1)

        raise TopScoreAPIError(f"All {self.max_retries} attempts failed") from last_exc

    @staticmethod
    def _handle_response(resp: Response) -> TopScoreResponse:
        status = resp.status_code
        if status == 429:
            raise TopScoreRateLimitError("Rate limit exceeded (429)")
        if status == 401:
            raise TopScoreAuthError("Unauthorized (401) – check credentials")
        if status == 404:
            raise TopScoreNotFoundError(f"Resource not found: {resp.url}")
        if status >= 400:
            try:
                body = resp.json()
                errors = body.get("errors", [resp.text])
            except ValueError:
                errors = [resp.text]
            raise TopScoreAPIError(f"API error {status}: {errors}")

        try:
            payload = resp.json()
        except ValueError as exc:
            raise TopScoreAPIError("Response is not valid JSON") from exc

        return TopScoreResponse(
            status=payload.get("status", status),
            result=payload.get("result", payload),
            count=payload.get("count"),
            errors=payload.get("errors", []),
            raw=payload,
        )

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        authenticated: bool = False,
    ) -> TopScoreResponse:
        """Perform a GET request."""
        return self._request("GET", endpoint, authenticated=authenticated, params=params)

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> TopScoreResponse:
        """Perform an authenticated POST request."""
        return self._request("POST", endpoint, authenticated=True, data=data, json=json)

    def get_all_pages(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        authenticated: bool = False,
        page_size: int = 50,
    ) -> List[Any]:
        """
        Fetch all pages for a paginated endpoint and return every result item.

        TopScore uses ``page`` (1-based) and ``per_page`` query parameters.
        """
        params = dict(params or {})
        params.setdefault("per_page", page_size)
        params["page"] = 1

        all_items: List[Any] = []
        while True:
            response = self.get(endpoint, params=params, authenticated=authenticated)
            items = response.result if isinstance(response.result, list) else [response.result]
            all_items.extend(items)

            # Stop when we received fewer items than a full page
            if len(items) < params["per_page"]:
                break
            params["page"] += 1
            logger.debug("Fetched page %s (%s items so far)", params["page"] - 1, len(all_items))

        return all_items

    def iter_pages(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        authenticated: bool = False,
        page_size: int = 50,
    ) -> Iterator[List[Any]]:
        """
        Yield one page of results at a time (as a list) for memory-efficient iteration.
        """
        params = dict(params or {})
        params.setdefault("per_page", page_size)
        params["page"] = 1

        while True:
            response = self.get(endpoint, params=params, authenticated=authenticated)
            items = response.result if isinstance(response.result, list) else [response.result]
            yield items
            if len(items) < params["per_page"]:
                break
            params["page"] += 1

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------

    def get_events(self, **params: Any) -> List[Any]:
        """Return all events. Pass keyword args as query-string filters."""
        return self.get_all_pages("events", params=params)

    def get_event(self, event_id: int) -> Any:
        """Return a single event by ID."""
        return self.get(f"events/{event_id}").result

    def create_event(self, **fields: Any) -> Any:
        """Create a new event (authenticated)."""
        return self.post("events", data=fields).result

    def update_event(self, event_id: int, **fields: Any) -> Any:
        """Update fields on an existing event (authenticated)."""
        return self.post(f"events/{event_id}", data=fields).result

    # ------------------------------------------------------------------
    # Teams
    # ------------------------------------------------------------------

    def get_teams(self, **params: Any) -> List[Any]:
        """Return all teams."""
        return self.get_all_pages("teams", params=params)

    def get_team(self, team_id: int) -> Any:
        """Return a single team by ID."""
        return self.get(f"teams/{team_id}").result

    def create_team(self, **fields: Any) -> Any:
        """Create a new team (authenticated)."""
        return self.post("teams", data=fields).result

    def update_team(self, team_id: int, **fields: Any) -> Any:
        """Update a team (authenticated)."""
        return self.post(f"teams/{team_id}", data=fields).result

    # ------------------------------------------------------------------
    # Games / Schedule
    # ------------------------------------------------------------------

    def get_games(self, **params: Any) -> List[Any]:
        """Return games. Filter by ``event_id``, ``team_id``, etc."""
        return self.get_all_pages("games", params=params)

    def get_game(self, game_id: int) -> Any:
        """Return a single game by ID."""
        return self.get(f"games/{game_id}").result

    def create_game(self, **fields: Any) -> Any:
        """Create a game (authenticated)."""
        return self.post("games", data=fields).result

    def update_game(self, game_id: int, **fields: Any) -> Any:
        """Update a game (authenticated). Common fields: ``start_time``, ``home_score``, etc."""
        return self.post(f"games/{game_id}", data=fields).result

    def report_score(
        self,
        game_id: int,
        home_score: int,
        away_score: int,
        **extra: Any,
    ) -> Any:
        """Convenience wrapper to submit a game score."""
        return self.update_game(
            game_id,
            home_score=home_score,
            away_score=away_score,
            **extra,
        )

    # ------------------------------------------------------------------
    # Registrations / Persons
    # ------------------------------------------------------------------

    def get_registrations(self, **params: Any) -> List[Any]:
        """Return registrations. Filter by ``event_id``, ``team_id``, etc."""
        return self.get_all_pages("registrations", params=params)

    def get_registration(self, registration_id: int) -> Any:
        return self.get(f"registrations/{registration_id}").result

    def get_persons(self, **params: Any) -> List[Any]:
        """Return person records (requires auth for non-public info)."""
        return self.get_all_pages("persons", params=params, authenticated=True)

    def get_person(self, person_id: int) -> Any:
        return self.get(f"persons/{person_id}", authenticated=True).result

    # ------------------------------------------------------------------
    # Locations / Fields
    # ------------------------------------------------------------------

    def get_locations(self, **params: Any) -> List[Any]:
        """Return locations."""
        return self.get_all_pages("locations", params=params)

    def get_location(self, location_id: int) -> Any:
        return self.get(f"locations/{location_id}").result

    # ------------------------------------------------------------------
    # Standings
    # ------------------------------------------------------------------

    def get_standings(self, event_id: int, **params: Any) -> List[Any]:
        """Return standings for an event."""
        params["event_id"] = event_id
        return self.get_all_pages("standings", params=params)

    # ------------------------------------------------------------------
    # Stages / Pools
    # ------------------------------------------------------------------

    def get_stages(self, **params: Any) -> List[Any]:
        return self.get_all_pages("stages", params=params)

    def get_stage(self, stage_id: int) -> Any:
        return self.get(f"stages/{stage_id}").result

    # ------------------------------------------------------------------
    # Messages
    # ------------------------------------------------------------------

    def send_message(
        self,
        subject: str,
        body: str,
        recipient_ids: Optional[List[int]] = None,
        **extra: Any,
    ) -> Any:
        """Send a message (authenticated). ``recipient_ids`` is optional."""
        payload = {"subject": subject, "body": body, **extra}
        if recipient_ids is not None:
            payload["recipient_ids"] = recipient_ids
        return self.post("messages", data=payload).result

    # ------------------------------------------------------------------
    # Raw / generic helpers
    # ------------------------------------------------------------------

    def raw_get(self, path: str, **params: Any) -> TopScoreResponse:
        """Make a raw GET to any ``/api/<path>`` endpoint."""
        return self.get(path, params=params)

    def raw_post(self, path: str, **fields: Any) -> TopScoreResponse:
        """Make a raw authenticated POST to any ``/api/<path>`` endpoint."""
        return self.post(path, data=fields)
