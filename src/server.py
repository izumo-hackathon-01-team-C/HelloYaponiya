from fastapi import FastAPI

from .routers import templates


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(templates.router)
    return app

app = create_app()