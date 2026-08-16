"""Pydantic schemas for web configuration DTOs."""
from __future__ import annotations

from typing import List, Optional, Union
from pydantic import BaseModel, Field


class PointDTO(BaseModel):
    x: float = Field(..., description="X coordinate (fraksi 0..1 atau piksel absolut)")
    y: float = Field(..., description="Y coordinate (fraksi 0..1 atau piksel absolut)")


class LineConfigDTO(BaseModel):
    start: PointDTO
    end: PointDTO
    orientation: str = Field(default="custom", description="v, h, atau custom")


class RoiConfigDTO(BaseModel):
    enabled: bool = Field(default=False)
    points: List[PointDTO] = Field(default_factory=list)


class StreamSourceDTO(BaseModel):
    source_type: str = Field(..., description="webcam, file, rtsp, atau demo")
    uri: Optional[Union[str, int]] = Field(default=0, description="Webcam index, path file, atau RTSP/HTTP URL")


class TrackerConfigDTO(BaseModel):
    tracker: str = Field(default="deepocsort", description="deepocsort, ocsort, atau lighttrack")
    conf_thresh: float = Field(default=0.3, ge=0.05, le=0.95)
    cooldown: int = Field(default=30, ge=1, le=300)


class ControlActionDTO(BaseModel):
    action: str = Field(..., description="reset, pause, resume, flip_direction")
