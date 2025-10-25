import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
from .db import engine
from .api.kyrgyz_adventure import router as tournament_router
from .db import engine

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    # Startup: Create database tables
    from .models.kyrgyz_adventure import Base  # Import here to avoid circular imports

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: Dispose of the engine
    await engine.dispose()


def create_app() -> FastAPI:
    debug = os.getenv("APP_ENV", "DEV") != "PROD"
    app = FastAPI(
        lifespan=lifespan,
        debug=debug,
        openapi_url="/openapi.json" if debug else None,
        docs_url="/docs" if debug else None,
        redoc_url="/redoc" if debug else None,
        title="Tournament App",
        version="0.1.0",
    )

    # Add SessionMiddleware
    secret_key = os.getenv("SECRET_KEY", "your-secure-secret-key")
    app.add_middleware(
        SessionMiddleware,
        secret_key=secret_key,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Restrict in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(tournament_router, prefix="/tournaments")

    return app
