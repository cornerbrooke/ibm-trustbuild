"""
IBM TrustBuild — Backend API Entry Point
FastAPI application server. Connects the React frontend to the
4-stage agent pipeline powered by watsonx.ai.
"""

import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.pipeline import router as pipeline_router

# ── Logging ──
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("trustbuild")

# ── App Setup ──
app = FastAPI(
    title="IBM TrustBuild API",
    description="The Idea-to-Deployment engine with compliance baked in.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ── CORS Middleware ──
# Allows the React frontend (running on localhost:3000) to call this API.
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://localhost:5173,http://localhost:8000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# ── Routes ──
app.include_router(pipeline_router)

# ── Root ──
@app.get("/")
async def root():
    return {
        "service": "IBM TrustBuild API",
        "version": "1.0.0",
        "endpoints": {
            "pipeline": "POST /api/run-pipeline",
            "health": "GET /api/health",
            "docs": "GET /docs"
        },
        "watsonx_mode": "simulation" if not os.getenv("WATSONX_API_KEY") else "live"
    }

# ── Startup Event ──
@app.on_event("startup")
async def on_startup():
    logger.info("=" * 60)
    logger.info("  IBM TrustBuild API — Starting Up")
    logger.info("=" * 60)
    logger.info(f"  Mode: {'LIVE (watsonx.ai)' if os.getenv('WATSONX_API_KEY') else 'SIMULATION'}")
    logger.info(f"  CORS Origins: {CORS_ORIGINS}")
    logger.info("  Endpoints:")
    logger.info("    POST /api/run-pipeline — Run the full TrustBuild pipeline")
    logger.info("    GET  /api/health       — Health check")
    logger.info("    GET  /docs             — Swagger UI")
    logger.info("=" * 60)
