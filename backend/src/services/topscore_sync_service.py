"""TopScore data synchronization service."""
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.integrations.topscore import TopScoreClient, TopScoreError
from src.models.league import League
from src.models.team import Team
from src.models.field import Field
from src.models.game import Game, GameStatus
from src.models.scrape_log import ScrapeLog, ScrapeStatus
from src.services.team_service import TeamService
from src.services.field_service import FieldService
from src.config.settings import settings

logger = logging.getLogger(__name__)


class TopScoreSyncService:
    """Service for synchronizing data from TopScore API to local database."""

    def __init__(self, db: Session):
        """Initialize the sync service."""
        self.db = db
        self.client = TopScoreClient(
            base_url=settings.TOPSCORE_BASE_URL,
            client_id=settings.TOPSCORE_CLIENT_ID,
            client_secret=settings.TOPSCORE_CLIENT_SECRET,
            csrf_token=settings.TOPSCORE_CSRF_TOKEN,
            timeout=settings.SCRAPER_TIMEOUT,
        )

    def sync_event_by_name(self, event_name_pattern: str) -> Dict[str, Any]:
        """
        Sync a single event by name pattern.

        Args:
            event_name_pattern: Case-insensitive name pattern to match

        Returns:
            Dict with sync statistics
        """
        logger.info(f"Searching for event matching: {event_name_pattern}")

        try:
            # Fetch all events and find matching one
            events = self.client.get_events()
            logger.info(f"Fetched {len(events)} events from TopScore")

            league_events = [e for e in events if e.get("type") == "league"]
            logger.info(f"Filtered to {len(league_events)} league events")

            pattern_lower = event_name_pattern.lower()
            matching_events = [
                e for e in league_events
                if pattern_lower in e.get('name', '').lower() or
                   pattern_lower in e.get('slug', '').lower()
            ]

            if not matching_events:
                logger.error(f"No event found matching '{event_name_pattern}'")
                return {
                    "leagues": 0,
                    "games": 0,
                    "teams": 0,
                    "fields": 0,
                    "errors": [f"No event found matching '{event_name_pattern}'"]
                }

            if len(matching_events) > 1:
                logger.warning(f"Found {len(matching_events)} matching events, using first match")
                for evt in matching_events:
                    logger.info(f"  - {evt.get('name')} (ID: {evt.get('id')})")

            event_data = matching_events[0]
            logger.info(f"Syncing event: {event_data.get('name')} (ID: {event_data.get('id')})")

            stats = {
                "leagues": 0,
                "games": 0,
                "teams": 0,
                "fields": 0,
                "errors": []
            }

            # Sync the event
            league, games_synced = self._sync_event(event_data)
            if league:
                stats["leagues"] = 1
                stats["games"] = games_synced

            self.db.commit()
            logger.info(f"Sync completed: {stats}")
            return stats

        except Exception as e:
            self.db.rollback()
            error_msg = f"Sync failed: {e}"
            logger.error(error_msg, exc_info=True)
            return {
                "leagues": 0,
                "games": 0,
                "teams": 0,
                "fields": 0,
                "errors": [error_msg]
            }

    def sync_all(self) -> Dict[str, Any]:
        """
        Sync all data from TopScore.

        Returns:
            Dict with sync statistics
        """
        logger.info("Starting full TopScore sync")
        start_time = datetime.utcnow()
        stats = {
            "leagues": 0,
            "teams": 0,
            "fields": 0,
            "games": 0,
            "errors": [],
        }

        try:
            # Sync events (leagues)
            events = self.client.get_events()
            logger.info(f"Fetched {len(events)} events from TopScore")

            league_events = [e for e in events if e.get("type") == "league"]
            logger.info(f"Filtered to {len(league_events)} league events (skipping {len(events) - len(league_events)} non-league events)")

            for event_data in league_events:
                try:
                    league, games_synced = self._sync_event(event_data)
                    if league:
                        stats["leagues"] += 1
                        stats["games"] += games_synced
                    self.db.commit()
                except Exception as e:
                    self.db.rollback()
                    error_msg = f"Error syncing event {event_data.get('id')}: {e}"
                    logger.error(error_msg)
                    stats["errors"].append(error_msg)

            self.db.commit()
            logger.info(f"Sync completed: {stats}")
            return stats

        except TopScoreError as e:
            self.db.rollback()
            error_msg = f"TopScore API error: {e}"
            logger.error(error_msg)
            stats["errors"].append(error_msg)
            raise
        except Exception as e:
            self.db.rollback()
            error_msg = f"Unexpected error during sync: {e}"
            logger.error(error_msg)
            stats["errors"].append(error_msg)
            raise

    def _sync_event(self, event_data: Dict[str, Any]) -> tuple[Optional[League], int]:
        """
        Sync a single event (league) and its games.

        Returns:
            Tuple of (League, number of games synced)
        """
        event_id = event_data.get("id")
        event_name = event_data.get("name", f"Event {event_id}")
        event_slug = event_data.get("slug", "")

        logger.info(f"Syncing event: {event_name} (ID: {event_id})")

        # Get or create league - use slug-based URL as unique identifier
        source_url = f"{settings.TOPSCORE_BASE_URL}/events/{event_slug or event_id}"

        league = self.db.query(League).filter(
            League.source_url == source_url
        ).first()

        if not league:
            league = League(
                name=event_name,
                source_url=source_url,
                is_active=event_data.get("status") == "active",
            )
            self.db.add(league)
            self.db.flush()
            logger.info(f"Created new league: {event_name}")
        else:
            # Update existing league
            league.name = event_name
            league.is_active = event_data.get("status") == "active"
            logger.info(f"Updated existing league: {event_name}")

        # Create scrape log
        scrape_log = ScrapeLog(
            league_id=league.id,
            started_at=datetime.utcnow(),
            status=ScrapeStatus.IN_PROGRESS,
            source_url=source_url,
        )
        self.db.add(scrape_log)
        self.db.flush()

        games_synced = 0
        try:
            # Fetch and sync games for this event
            games = self.client.get_games(event_id=event_id)
            logger.info(f"Fetched {len(games)} games for event {event_id}")

            for game_data in games:
                if self._sync_game(game_data, league):
                    games_synced += 1

            # Update scrape log as completed
            scrape_log.completed_at = datetime.utcnow()
            scrape_log.status = ScrapeStatus.SUCCESS
            scrape_log.games_found = games_synced
            scrape_log.games_created = games_synced  # Simplified for now

        except Exception as e:
            scrape_log.completed_at = datetime.utcnow()
            scrape_log.status = ScrapeStatus.FAILED
            scrape_log.error_message = str(e)
            raise

        return league, games_synced

    def _sync_game(self, game_data: Dict[str, Any], league: League) -> bool:
        """
        Sync a single game to the database.

        Returns:
            True if game was synced successfully
        """
        game_id = game_data.get("id")
        external_id = str(game_id)

        # Check if game already exists
        existing_game = self.db.query(Game).filter(
            Game.league_id == league.id,
            Game.external_id == external_id
        ).first()

        # Get or create teams (try both capitalized and lowercase keys)
        home_team_data = game_data.get("HomeTeam") or game_data.get("home_team", {})
        away_team_data = game_data.get("AwayTeam") or game_data.get("away_team", {})

        if not home_team_data or not away_team_data:
            logger.warning(f"Game {game_id} missing team data, skipping")
            return False

        home_team = self._get_or_create_team(home_team_data)
        away_team = self._get_or_create_team(away_team_data)

        # Get or create field
        field = None
        location_data = game_data.get("location")
        field_name = game_data.get("field_name")

        if location_data and isinstance(location_data, dict):
            field = self._get_or_create_field(location_data)
        elif field_name:
            # Create field from field_name if no location object exists
            # Convert to string if needed (API sometimes returns integers)
            field = self._get_or_create_field({"name": str(field_name)})

        # Parse game date and time
        game_date = None
        game_time = None

        # Try parsing combined datetime first, then separate date/time fields
        start_datetime = game_data.get("start_datetime") or game_data.get("start_datetime_tz")
        if start_datetime:
            try:
                dt = datetime.fromisoformat(start_datetime.replace('Z', '+00:00'))
                game_date = dt.date()
                game_time = dt.time()
            except (ValueError, AttributeError):
                pass

        # If no combined datetime, try separate fields
        if not game_date:
            start_date_str = game_data.get("start_date")
            start_time_str = game_data.get("start_time")

            if start_date_str:
                try:
                    game_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                except (ValueError, TypeError):
                    logger.warning(f"Invalid start_date for game {game_id}: {start_date_str}")

            if start_time_str:
                try:
                    game_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
                except (ValueError, TypeError):
                    logger.warning(f"Invalid start_time for game {game_id}: {start_time_str}")

        # Determine game status
        status = GameStatus.UPCOMING
        if game_data.get("is_played") or game_data.get("status") in ["has_outcome", "final"]:
            status = GameStatus.COMPLETED
        elif game_data.get("status") == "cancelled":
            status = GameStatus.CANCELLED

        # Get scores
        home_score = game_data.get("home_score")
        away_score = game_data.get("away_score")

        if existing_game:
            # Update existing game
            existing_game.game_date = game_date or existing_game.game_date
            existing_game.game_time = game_time
            existing_game.home_score = home_score
            existing_game.away_score = away_score
            existing_game.status = status
            existing_game.field_id = field.id if field else existing_game.field_id
            existing_game.scraped_at = datetime.utcnow()
        else:
            # Create new game
            game = Game(
                league_id=league.id,
                home_team_id=home_team.id,
                away_team_id=away_team.id,
                field_id=field.id if field else None,
                game_date=game_date or datetime.utcnow().date(),
                game_time=game_time,
                home_score=home_score,
                away_score=away_score,
                status=status,
                external_id=external_id,
                scraped_at=datetime.utcnow(),
            )
            self.db.add(game)

        return True

    def _get_or_create_team(self, team_data: Dict[str, Any]) -> Team:
        """Get or create a team from TopScore data."""
        team_name = team_data.get("name") or team_data.get("label", "Unknown Team")
        return TeamService.get_or_create_team(self.db, team_name)

    def _get_or_create_field(self, location_data: Dict[str, Any]) -> Field:
        """Get or create a field from TopScore location data."""
        field_name = location_data.get("name", "Unknown Field")
        if not isinstance(field_name, str):
            field_name = str(field_name) if field_name else "Unknown Field"
        address = location_data.get("address")
        city = location_data.get("city")
        return FieldService.get_or_create_field(self.db, field_name, address, city)
