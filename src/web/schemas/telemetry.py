"""Pydantic schemas for telemetry and object detection tracking DTOs."""
from __future__ import annotations

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from src.web.schemas.config import PointDTO, LineConfigDTO, RoiConfigDTO


class TrackBoxDTO(BaseModel):
    track_id: int
    x1: float
    y1: float
    x2: float
    y2: float
    cx: float
    cy: float
    is_in_roi: bool = True
    color_hex: str = "#10B981"


class TrafficPointDTO(BaseModel):
    timestamp_sec: float
    total: int
    count_in: int
    count_out: int
    occupancy: int


class TelemetryPayload(BaseModel):
    timestamp: float
    status: str = Field(default="active", description="active, paused, disconnected, error")
    fps: float
    latency_ms: float
    total_count: int
    count_in: int
    count_out: int
    live_occupancy: int
    line: LineConfigDTO
    roi: RoiConfigDTO
    tracks: List[TrackBoxDTO] = Field(default_factory=list)
    recent_traffic: List[TrafficPointDTO] = Field(default_factory=list)
    source_name: str = "Webcam 0"
    model_name: str = "YOLO26-S + Deep-OC-SORT"
