"""Telemetry Hub for aggregating real-time analytics and rolling time-series."""
from __future__ import annotations

import collections
import time
from typing import Any, Dict, List

from src.web.schemas.telemetry import (
    PointDTO,
    LineConfigDTO,
    RoiConfigDTO,
    TrackBoxDTO,
    TrafficPointDTO,
    TelemetryPayload,
)


class TelemetryHub:
    """Mengelola akumulasi metrik real-time, FPS smoothing, dan riwayat arus per detik."""

    def __init__(self, max_history_seconds: int = 60):
        self._fps: float = 0.0
        self._latency_ms: float = 0.0
        self._total_count: int = 0
        self._count_in: int = 0
        self._count_out: int = 0
        self._live_occupancy: int = 0
        self._status: str = "active"
        self._source_name: str = "Webcam 0"
        self._model_name: str = "YOLO26-S + Deep-OC-SORT"

        # Simpan riwayat trafik per interval
        self._traffic_history: collections.deque[TrafficPointDTO] = collections.deque(maxlen=max_history_seconds)
        self._last_history_tick = 0.0

    def update_performance(self, latency_ms: float) -> None:
        """Pembaruan metrik latensi dan FPS dengan Exponential Moving Average."""
        self._latency_ms = latency_ms
        instant_fps = 1000.0 / max(latency_ms, 1e-6)
        if self._fps == 0.0:
            self._fps = instant_fps
        else:
            self._fps = 0.85 * self._fps + 0.15 * instant_fps

    def update_counts(self, total: int, count_in: int, count_out: int, occupancy: int) -> None:
        """Pembaruan angka hitungan dari PeopleCounter."""
        self._total_count = total
        self._count_in = count_in
        self._count_out = count_out
        self._live_occupancy = occupancy

        now = time.time()
        # Catat 1 titik grafik setiap 1 detik
        if now - self._last_history_tick >= 1.0:
            self._last_history_tick = now
            self._traffic_history.append(
                TrafficPointDTO(
                    timestamp_sec=now,
                    total=total,
                    count_in=count_in,
                    count_out=count_out,
                    occupancy=occupancy,
                )
            )

    def set_source_and_model(self, source_name: str, model_name: str) -> None:
        self._source_name = source_name
        self._model_name = model_name

    def set_status(self, status: str) -> None:
        self._status = status

    def reset_history(self) -> None:
        self._traffic_history.clear()
        self._total_count = 0
        self._count_in = 0
        self._count_out = 0
        self._live_occupancy = 0

    def build_payload(
        self,
        line: LineConfigDTO,
        roi: RoiConfigDTO,
        tracks: List[TrackBoxDTO],
    ) -> TelemetryPayload:
        """Bentuk objek TelemetryPayload lengkap untuk dikirimkan via WebSocket."""
        return TelemetryPayload(
            timestamp=time.time(),
            status=self._status,
            fps=round(self._fps, 1),
            latency_ms=round(self._latency_ms, 1),
            total_count=self._total_count,
            count_in=self._count_in,
            count_out=self._count_out,
            live_occupancy=self._live_occupancy,
            line=line,
            roi=roi,
            tracks=tracks,
            recent_traffic=list(self._traffic_history),
            source_name=self._source_name,
            model_name=self._model_name,
        )
