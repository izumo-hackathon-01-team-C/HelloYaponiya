import csv

from fastapi import FastAPI

from tortoise import Tortoise

from src.routers.templates import templates
from src.routers.translations import translations

from src.settings import settings


async def create_db_client() -> Tortoise:
    db_client = Tortoise()
    await db_client.init(
        db_url=settings.db_uri,
        modules={
            'models': ['src.database.models']
        }
    )

    return db_client


def prepare_fixtures() -> dict:
    with open('src/fixtures/formatted_locales.csv') as file:
        reader = csv.DictReader(file)

        translation_fixtures = {}
        for row in reader:
            lang_dict = translation_fixtures.setdefault(row['iso_lang'], {})
            lang_dict[row['key']] = row['value']
    return translation_fixtures


def create_app() -> FastAPI:
    app = FastAPI(debug=True)

    app.include_router(templates.router)
    app.include_router(translations.router)

    @app.on_event('startup')
    async def startup() -> None:
        app.state.db = await create_db_client()
        await app.state.db.generate_schemas()

        app.state.translation_fixtures = prepare_fixtures()

    @app.on_event('shutdown')
    async def shutdown() -> None:
        await app.state.db.close_connections()

    return app


app = create_app()
