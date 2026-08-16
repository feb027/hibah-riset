"""Streaming routes for video feed."""
from __future__ import annotations

import asyncio
import time
from typing import AsyncGenerator

import cv2
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/api/stream", tags=["stream"])


@router.get("/video_feed")
async def video_feed(request: Request) -> StreamingResponse:
    """Menyediakan aliran video real-time berformat MJPEG Multipart."""
    pipeline = request.app.state.pipeline
    stream_mgr = request.app.state.stream_mgr

    async def frame_generator() -> AsyncGenerator[bytes, None]:
        while True:
            # Cek jika klien terputus
            if await request.is_disconnected():
                break

            frame = stream_mgr.read_frame()
            if frame is None:
                await asyncio.sleep(0.02)
                continue

            # Jalankan inferensi AI
            annotated_frame, telemetry = pipeline.process_frame(frame)

            # Encode ke JPEG berkualitas tinggi namun ringan
            ret, buffer = cv2.imencode(".jpg", annotated_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            if not ret:
                await asyncio.sleep(0.01)
                continue

            frame_bytes = buffer.tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n"
                b"Content-Length: " + str(len(frame_bytes)).encode() + b"\r\n\r\n"
                + frame_bytes + b"\r\n"
            )
            # Throttle halus agar tidak membebani network
            await asyncio.sleep(0.015)

    return StreamingResponse(
        frame_generator(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


@router.post("/upload_frame")
async def upload_frame(request: Request):
    """Menerima frame biner (JPEG) dari kamera HP atau webcam browser klien."""
    stream_mgr = request.app.state.stream_mgr
    body = await request.body()
    if not body:
        return {"status": "error", "message": "Body kosong"}

    nparr = np.frombuffer(body, np.uint8)
    frame_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if frame_bgr is not None:
        stream_mgr.feed_client_frame(frame_bgr)
        return {"status": "ok"}
    return {"status": "error", "message": "Gagal decode frame"}

