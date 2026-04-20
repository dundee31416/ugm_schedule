"""Sync API endpoints."""
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any

from src.database.session import get_db
from src.services.topscore_sync_service import TopScoreSyncService
from src.utils.logger import logger

router = APIRouter()


@router.post("/topscore")
async def trigger_topscore_sync(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> Dict[str, str]:
    """
    Trigger a sync from TopScore API.

    The sync runs in the background to avoid blocking the request.
    """
    def run_sync():
        """Background task to run the sync."""
        db_session = next(get_db())
        try:
            sync_service = TopScoreSyncService(db_session)
            stats = sync_service.sync_all()
            logger.info(f"Background sync completed: {stats}")
        except Exception as e:
            logger.error(f"Background sync failed: {e}", exc_info=True)
        finally:
            db_session.close()

    background_tasks.add_task(run_sync)

    return {
        "status": "started",
        "message": "TopScore sync has been started in the background"
    }


@router.post("/topscore/immediate")
def trigger_topscore_sync_immediate(
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    Trigger an immediate sync from TopScore API.

    WARNING: This runs synchronously and will block until complete.
    Use the /sync/topscore endpoint for background execution.
    """
    try:
        sync_service = TopScoreSyncService(db)
        stats = sync_service.sync_all()

        return {
            "status": "completed",
            "message": "TopScore sync completed successfully",
            "stats": stats
        }
    except Exception as e:
        logger.error(f"Sync failed: {e}", exc_info=True)
        return {
            "status": "failed",
            "message": f"Sync failed: {str(e)}",
            "stats": None
        }
