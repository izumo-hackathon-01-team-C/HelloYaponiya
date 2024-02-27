from pydantic import BaseConfig, AnyUrl


class Settings(BaseConfig):
    db_uri: AnyUrl = 'sqlite://db.sqlite3'


settings = Settings()
