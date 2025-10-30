import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager

from starlette.staticfiles import StaticFiles

from .db import engine


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    # Startup: Create database tables
    from .models.kyrgyz_adventure import Base

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
        title="Kyrgyz Adventure App",  # Updated title
        version="0.1.0",
    )

    current_dir = os.path.dirname(os.path.realpath(__file__))
    static_dir = os.path.join(current_dir, "static")
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    secret_key = os.getenv("SECRET_KEY", "your-secure-secret-key")
    app.add_middleware(SessionMiddleware, secret_key=secret_key)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from .core.main import router as main_pages_router

    app.include_router(main_pages_router, tags=["Main Pages"])

    return app
