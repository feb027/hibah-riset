"""REST API endpoints for configuration and control mutations."""
from __future__ import annotations

from typing import Any, Dict
from fastapi import APIRouter, HTTPException, Request

from src.web.schemas.config import (
    ControlActionDTO,
    LineConfigDTO,
    RoiConfigDTO,
    StreamSourceDTO,
    TrackerConfigDTO,
)

router = APIRouter(prefix="/api", tags=["config"])


@router.get("/config")
async def get_config(request: Request) -> Dict[str, Any]:
    """Mendapatkan konfigurasi sistem aktif."""
    pipeline = request.app.state.pipeline
    stream_mgr = request.app.state.stream_mgr
    return {
        "line": pipeline.line_dto.model_dump(),
        "roi": pipeline.roi_dto.model_dump(),
        "source": {
            "name": stream_mgr.source_name,
            "dimensions": list(stream_mgr.dimensions),
        },
        "tracker": {
            "name": pipeline.tracker_name,
            "conf_thresh": pipeline.conf_thresh,
            "cooldown": pipeline.cooldown,
        },
    }


@router.post("/config/line")
async def update_line(config: LineConfigDTO, request: Request) -> Dict[str, Any]:
    """Memperbarui koordinat garis virtual counting secara dinamis."""
    pipeline = request.app.state.pipeline
    pipeline.set_line(config.start, config.end, config.orientation)
    return {"status": "success", "message": "Garis virtual berhasil diperbarui", "line": pipeline.line_dto.model_dump()}


@router.post("/config/roi")
async def update_roi(config: RoiConfigDTO, request: Request) -> Dict[str, Any]:
    """Memperbarui poligon zona RoI aktif."""
    pipeline = request.app.state.pipeline
    pipeline.set_roi(config.points, config.enabled)
    return {"status": "success", "message": "Zona RoI berhasil diperbarui", "roi": pipeline.roi_dto.model_dump()}


@router.post("/control/action")
async def trigger_action(action_dto: ControlActionDTO, request: Request) -> Dict[str, Any]:
    """Memicu aksi kontrol: reset, flip_direction, pause, resume."""
    pipeline = request.app.state.pipeline
    action = action_dto.action.lower()

    if action == "reset":
        pipeline.reset_counts()
        return {"status": "success", "message": "Hitungan berhasil di-reset ke 0"}
    elif action == "flip_direction":
        pipeline.flip_direction()
        return {"status": "success", "message": "Arah garis berhasil dibalik"}
    elif action == "pause":
        pipeline.telemetry_hub.set_status("paused")
        return {"status": "success", "message": "Sistem di-pause"}
    elif action == "resume":
        pipeline.telemetry_hub.set_status("active")
        return {"status": "success", "message": "Sistem dilanjutkan"}
    else:
        raise HTTPException(status_code=400, detail=f"Aksi '{action}' tidak dikenal")


@router.post("/control/source")
async def change_source(source_dto: StreamSourceDTO, request: Request) -> Dict[str, Any]:
    """Mengubah sumber video input secara dinamis (Webcam, File, RTSP)."""
    stream_mgr = request.app.state.stream_mgr
    pipeline = request.app.state.pipeline

    src_uri = source_dto.uri
    ok = stream_mgr.set_source(src_uri)
    if not ok:
        raise HTTPException(status_code=400, detail=f"Gagal menghubungkan ke sumber video: {src_uri}")

    pipeline.telemetry_hub.set_source_and_model(stream_mgr.source_name, f"YOLO26-S + {pipeline.tracker_name.upper()}")
    return {
        "status": "success",
        "message": f"Sumber video berhasil diubah ke {stream_mgr.source_name}",
        "dimensions": list(stream_mgr.dimensions),
    }
