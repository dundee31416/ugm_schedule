"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.config.settings import settings
from src.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting UGM Schedule API")
    logger.info(f"CORS origins: {settings.cors_origins_list}")
    yield
    # Shutdown
    logger.info("Shutting down UGM Schedule API")


# Create FastAPI application
app = FastAPI(
    title="UGM Schedule API",
    description="API for scraping and displaying sports league schedules",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.1.0"
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "UGM Schedule API",
        "docs": "/docs",
        "health": "/api/health"
    }


# Import and include routers
from src.api.v1 import api_router

app.include_router(api_router, prefix="/api/v1")
