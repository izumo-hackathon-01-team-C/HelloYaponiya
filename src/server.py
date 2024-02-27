import csv
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


def prepare_fixtures(app: FastAPI) -> None:
    with open('src/fixtures/formatted_locales.csv') as file:
        reader = csv.DictReader(file)

        translation_fixtures = {}
        for row in reader:
            lang_dict = translation_fixtures.setdefault(row['iso_lang'], {})
            lang_dict[row['key']] = row['value']

    app.state.translation_fixtures = translation_fixtures

    class FileManager:
        def __init__(self, file_pairs: dict):
            self.file_pairs = file_pairs

        def get_file_by_form_name(self, form_name: str, file_type: str) -> bytes | None:
            if file_path := self.file_pairs.get(form_name, {}).get(file_type):
                with open(file_path, 'rb') as file:
                    return file.read()

    with open('src/fixtures/form_pairs.json') as file:
        forms_pairs = json.load(file)

    app.state.file_manager = FileManager(forms_pairs)


def create_app() -> FastAPI:
    app = FastAPI(debug=True)

    app.include_router(templates.router, tags=['Templates'])
    app.include_router(translations.router, tags=['Translations'])
    # CORS
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    @app.on_event('startup')
    async def startup() -> None:
        app.state.db = await create_db_client()
        await app.state.db.generate_schemas()

        prepare_fixtures(app)


    @app.on_event('shutdown')
    async def shutdown() -> None:
        await app.state.db.close_connections()

    return app


app = create_app()
