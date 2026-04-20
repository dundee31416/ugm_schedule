"""Logging configuration for the application."""
import logging
import sys
from typing import Any

from src.config.settings import settings


def setup_logging() -> logging.Logger:
    """Configure and return application logger."""
    # Create logger
    logger = logging.getLogger("ugm_schedule")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))

    # Remove existing handlers
    logger.handlers.clear()

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, settings.LOG_LEVEL))

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger


# Global logger instance
logger = setup_logging()


def log_info(message: str, **kwargs: Any) -> None:
    """Log info message with optional context."""
    logger.info(message, extra=kwargs)


def log_error(message: str, **kwargs: Any) -> None:
    """Log error message with optional context."""
    logger.error(message, extra=kwargs)


def log_warning(message: str, **kwargs: Any) -> None:
    """Log warning message with optional context."""
    logger.warning(message, extra=kwargs)


def log_debug(message: str, **kwargs: Any) -> None:
    """Log debug message with optional context."""
    logger.debug(message, extra=kwargs)
