"""Web schemas package."""
from src.web.schemas.config import (
    PointDTO,
    LineConfigDTO,
    RoiConfigDTO,
    StreamSourceDTO,
    TrackerConfigDTO,
    ControlActionDTO,
)
from src.web.schemas.telemetry import (
    TrackBoxDTO,
    TrafficPointDTO,
    TelemetryPayload,
)

__all__ = [
    "PointDTO",
    "LineConfigDTO",
    "RoiConfigDTO",
    "StreamSourceDTO",
    "TrackerConfigDTO",
    "ControlActionDTO",
    "TrackBoxDTO",
    "TrafficPointDTO",
    "TelemetryPayload",
]
