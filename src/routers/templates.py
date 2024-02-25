import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from pydantic import BaseModel

import fastapi
from fastapi import Request
from fastapi.routing import APIRouter

router = APIRouter()


# Interfaces
class FormTemplate(ABC):
    """Abstract template for form processing"""

    @abstractmethod
    def fill(self, **kwargs):
        """"A function to fill existing form with user's data stated in kwargs"""
        raise NotImplemented


# API Models
class TemplateBuildSources(BaseModel):
    name: str
    markup_json: str
    localization_json: str
    metadata_json: str
    template_xlsx_file: bytes


# Models
@dataclass
class MarkedTemplate(FormTemplate):
    """A class to take user's localized input, de-localize it and fill both JP/Local forms"""
    pass


@dataclass
class Localization:
    """Adalo app's textfield's localizations distinguished by 'name' key"""
    name: str
    lang: str
    value: str


@dataclass
class Category:
    """Adalos app's section's nested divisions"""
    forms: list[str] = field(default_factory=list)


@dataclass
class Section:
    """Adalos app's main screen section [e.g. Health, Taxes and so on]"""
    categories: list[Category] = field(default_factory=list)


@router.post(path="/template/create")
def create_template(request: Request, source: TemplateBuildSources) -> str:
    """A method to create template for form in Adalo/PythonServer"""

    if source.name in request.app.templates.keys():
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                                    detail=f"Template with name '{source.name}' already exists. "
                                           "To update it use '/temlate/update' endpoint")

    return json.dumps(dict())


@router.post(path="/template/update")
def update_template(request: Request, source: TemplateBuildSources) -> str:
    """"""
    if source.name == "" or source.name == None:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                                    detail="No name provided")
    return json.dumps(dict())
