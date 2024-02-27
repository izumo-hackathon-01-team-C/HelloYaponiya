from pydantic import BaseConfig, AnyUrl


class Settings(BaseConfig):
    db_uri: AnyUrl = 'sqlite://db.sqlite3'
    debug: bool = True
    translation_api_key: str


settings = Settings()
