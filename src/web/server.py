"""FastAPI Application Server Entrypoint for People Counting Web Dashboard."""
from __future__ import annotations

import argparse
import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.web.api.routes_config import router as config_router  # noqa: E402
from src.web.api.routes_stream import router as stream_router  # noqa: E402
from src.web.api.routes_telemetry import router as telemetry_router  # noqa: E402
from src.web.core.pipeline import EnginePipeline  # noqa: E402
from src.web.core.stream_manager import StreamManager  # noqa: E402


def create_app(source: str = "0", tracker: str = "deepocsort", weights: str = None) -> FastAPI:
    """Factory pembuat aplikasi FastAPI dengan dependensi state terinjeksi."""
    STATIC_DIR = Path(__file__).parent / "static"

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup: Inisialisasi sumber stream dan pipeline AI
        src_val = int(source) if source.isdigit() else source
        stream_mgr = StreamManager(source=src_val)
        stream_mgr.start()

        pipeline = EnginePipeline(
            weights_path=weights or str(ROOT / "data" / "s2" / "weights" / "best.onnx"),
            tracker_name=tracker,
        )

        app.state.stream_mgr = stream_mgr
        app.state.pipeline = pipeline
        print("[Server] Layanan People Counting Web Dashboard siap!")
        yield
        # Shutdown
        stream_mgr.stop()
        print("[Server] Layanan dimatikan dengan aman.")

    app = FastAPI(
        title="Real-Time People Counting System",
        description="Modular & Scalable Web Dashboard for Real-Time People Counting Analytics",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount API Routers
    app.include_router(config_router)
    app.include_router(stream_router)
    app.include_router(telemetry_router)

    # Mount Static Web Client
    if STATIC_DIR.is_dir():
        app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

    return app


def parse_args():
    p = argparse.ArgumentParser(description="Jalankan Web Dashboard Real-Time People Counting")
    p.add_argument("--host", default="0.0.0.0", help="Host binding (0.0.0.0 untuk akses Tailscale/LAN)")
    p.add_argument("--port", type=int, default=8000, help="Port server (default: 8000)")
    p.add_argument("--source", default="0", help="Sumber video: webcam index (0), video.mp4, atau URL RTSP")
    p.add_argument("--tracker", default="deepocsort", choices=["deepocsort", "ocsort", "lighttrack"])
    p.add_argument("--weights", default=str(ROOT / "data" / "s2" / "weights" / "best.onnx"))
    return p.parse_args()


if __name__ == "__main__":
    import uvicorn
    args = parse_args()
    app = create_app(source=args.source, tracker=args.tracker, weights=args.weights)
    print(f"\n==================================================================")
    print(f"  PEOPLE COUNTING WEB DASHBOARD BERJALAN")
    print(f"  Akses Lokal     : http://localhost:{args.port}")
    print(f"  Akses Tailscale : http://<IP-Tailscale>:{args.port}")
    print(f"  Sumber Video    : {args.source}")
    print(f"  Tracker Aktif   : {args.tracker.upper()}")
    print(f"==================================================================\n")
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")
