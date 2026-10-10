from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.errors import register_exception_handlers
from api.routers import questionnaires_router
from infrastructure.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Действие при остановке приложения — закрываем пул соединений
    await engine.dispose()

def create_app() -> FastAPI:
    app = FastAPI(
        title="Medical questionnaires",
        description="Read-only backend-приложение для отдачи медицинских анкет.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    app.include_router(questionnaires_router, prefix="/api/v1")
    register_exception_handlers(app)
    return app