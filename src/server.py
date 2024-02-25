from fastapi import FastAPI

from routers import templates


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(templates.router)

    # Server globals
    #TODO: push to App
    app.state.templates = {}  #       dict[ str, MarkedTemplate ]
    app.state.localizations: dict = {}  # :     dict[ str, Localization ]
    app.state.sections: list = [] # :     list[ Section ]

    return app
