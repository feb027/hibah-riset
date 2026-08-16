"""Web API routes."""
from src.web.api.routes_config import router as config_router
from src.web.api.routes_stream import router as stream_router
from src.web.api.routes_telemetry import router as telemetry_router

__all__ = ["config_router", "stream_router", "telemetry_router"]
