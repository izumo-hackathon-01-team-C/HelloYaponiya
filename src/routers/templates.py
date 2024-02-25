import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel

import fastapi
from fastapi import Request
from fastapi.routing import APIRouter

from src.database.models import FormTemplateDBModel

router = APIRouter()

# Enums
class Languages( StrEnum ):
    Japanese = "jp"
    English  = "en"
    Russian  = "ru"
    Spain    = "sp"
    Brasil   = "br"
    Chineese = "cn"
    French   = "fr"
    Vietnamese = "vn"
    Cambodian  = "cn"
    Thai       = "??"

# Interfaces
class FormTemplate(ABC):
    """Abstract template for form processing"""

    @abstractmethod
    def fill(self, **kwargs):
        """"A function to fill existing form with user's data stated in kwargs"""
        raise NotImplemented


# API Models
class TemplateBuildSources(BaseModel):
    """Data for building documents templates and storing them in app's structure"""
    name: str
    description: str
    markup_data: str
    localization_json: str
    metadata_json: str
    excel_data: bytes

class Metadata( BaseModel ):
    """Metadata for versioning and organizing structure"""
    name: str
    category: str
    section: str
    creation_datetime: datetime
    update_datetime: datetime

class TemplateFillerData( BaseModel ):
    """Data for filling form template"""
    lang: Languages
    json: str

class FillupResult( BaseModel ):
    lang:   Languages
    jp:     bytes
    local:  bytes

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

    if source.name in request.app.state.db.templates.keys(): #TODO: set actual name
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                                    detail=f"Template with name '{source.name}' already exists. "
                                           "To update it use '/temlate/update' endpoint")
    
    FormTemplateDBModel.
    source.name
    source.template_xlsx_file
    source.markup_json
     
    return json.dumps(dict())


@router.post(path="/template/update")
def update_template(request: Request, source: TemplateBuildSources) -> str:
    """"""
    if source.name == "" or source.name == None:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                                    detail="No name provided")
    return json.dumps(dict())

@router.get( path="/template/fillup/{form_id}" )
def fillup( request: Request, form_id: str, in_data: TemplateFillerData ) -> FillupResult:
    return FillupResult( lang=in_data.lang, jp=None, local=None)