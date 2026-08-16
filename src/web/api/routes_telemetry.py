"""WebSocket endpoint for real-time telemetry streaming."""
from __future__ import annotations

import asyncio
import json
from typing import Set

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["telemetry"])


class ConnectionManager:
    """Mengelola koneksi WebSocket multi-klien secara thread-safe."""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self.active_connections.add(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            self.active_connections.discard(websocket)

    async def broadcast(self, message: str) -> None:
        dead_connections = set()
        async with self._lock:
            for connection in list(self.active_connections):
                try:
                    await connection.send_text(message)
                except Exception:
                    dead_connections.add(connection)
            for dead in dead_connections:
                self.active_connections.discard(dead)


manager = ConnectionManager()


@router.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket) -> None:
    """Kanal WebSocket telemetri real-time untuk pembaruan metrik, garis, dan kotak deteksi."""
    await manager.connect(websocket)
    pipeline = websocket.app.state.pipeline

    try:
        while True:
            # Kirim data telemetri terbaru setiap 50 ms (20 Hz)
            payload = pipeline.telemetry_hub.build_payload(
                line=pipeline.line_dto,
                roi=pipeline.roi_dto,
                tracks=[],
            )
            await websocket.send_text(payload.model_dump_json())
            await asyncio.sleep(0.05)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception:
        await manager.disconnect(websocket)
