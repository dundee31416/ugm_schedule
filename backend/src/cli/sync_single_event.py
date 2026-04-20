#!/usr/bin/env python
"""
CLI script to sync a single event from TopScore API.

Usage:
    python -m src.cli.sync_single_event "ligues-recreatives-hiver-2025-2026"
"""
import logging
import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.database.session import SessionLocal
from src.services.topscore_sync_service import TopScoreSyncService
from src.config.settings import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Run the TopScore sync for a single event."""
    if len(sys.argv) < 2:
        logger.error("Usage: python -m src.cli.sync_single_event <event_name_pattern>")
        logger.error("Example: python -m src.cli.sync_single_event 'ligues-recreatives-hiver-2025'")
        sys.exit(1)

    event_pattern = sys.argv[1]

    logger.info("=" * 70)
    logger.info(f"TopScore Single Event Sync: {event_pattern}")
    logger.info("=" * 70)

    # Validate credentials
    if not settings.TOPSCORE_CLIENT_ID or not settings.TOPSCORE_CLIENT_SECRET:
        logger.error("TopScore credentials not configured!")
        logger.error("Please set TOPSCORE_CLIENT_ID and TOPSCORE_CLIENT_SECRET in your .env file")
        sys.exit(1)

    db = SessionLocal()
    try:
        sync_service = TopScoreSyncService(db)
        stats = sync_service.sync_event_by_name(event_pattern)

        logger.info("=" * 70)
        logger.info("Sync Summary:")
        logger.info(f"  Leagues synced: {stats['leagues']}")
        logger.info(f"  Games synced: {stats['games']}")

        if stats['errors']:
            logger.warning(f"  Errors encountered: {len(stats['errors'])}")
            for error in stats['errors']:
                logger.error(f"    - {error}")
        else:
            logger.info("  No errors encountered")

        logger.info("=" * 70)
        if stats['leagues'] > 0:
            logger.info("Single Event Sync Completed Successfully")
        else:
            logger.warning("No data was synced")
        logger.info("=" * 70)

    except Exception as e:
        logger.error("=" * 70)
        logger.error(f"Sync failed with error: {e}", exc_info=True)
        logger.error("=" * 70)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
