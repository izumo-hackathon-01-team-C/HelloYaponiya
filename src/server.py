from fastapi import FastAPI

from tortoise import Tortoise

from routers import templates
from settings import settings


async def create_db_client() -> Tortoise:
    db_client = Tortoise()
    await db_client.init(
        db_url=settings.db_uri,
        modules={
            'models': ['database.models']
        }
    )

    return db_client


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(templates.router)

    @app.on_event('startup')
    async def startup() -> None:
        app.state.db = await create_db_client()
        await app.state.db.generate_schemas()

    return app


app = create_app()
