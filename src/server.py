from typing import BinaryIO
import fastapi


import json
from datetime import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pydantic import BaseModel


app = fastapi.FastAPI()

# Interfaces
class FormTemplate( ABC ):
    """Abstract template for form processing"""
    @abstractmethod
    def fill( self, **kwargs ):
        """"A function to fill existing form with user's data stated in kwargs"""
        raise NotImplemented

# API Models
class TemplateBuildSources( BaseModel ):
    name: str
    markup_json: str
    localization_json: str
    metadata_json: str
    template_xlsx_file: bytes 

class Metadata( BaseModel ):
    """Template metadata for versioning and """
    name: str
    cathegory: str
    section: str
    creation_datetime: datetime
    update_datetime: datetime

# Models
@dataclass
class MarkedTemplate( FormTemplate ): 
    """A class to take user's localized input, de-localize it and fill both JP/Local forms"""
    pass



@dataclass
class Localization:
    """Adalo app's textfield's localizations distinguished by 'name' key"""
    name: str
    lang: str
    value: str

@dataclass
class Cathegory:
    """Adalos app's section's nested divisions"""
    name: str 
    forms: list[ str ] = field( default_factory=list )    

@dataclass
class Section:
    """Adalos app's main screen section [e.g. Health, Taxes and so on]"""
    name: str
    cathegories: list[ Cathegory ] = field( default_factory=list )

# Server globals
#TODO: push to App
app.templates       = {} #       dict[ str, MarkedTemplate ]    
app.localizations   = {} # :     dict[ str, Localization ]       
app.sections        = [] # :     list[ Section ]                 
#TODO: recycling_bin for deleted objects?

# API Endpoints
@app.post( path="/template/create" )
def create_template( source: TemplateBuildSources ) -> str:
    """A method to create template for form in Adalo/PythonServer"""

    if source.name in app.templates.keys(): 
        raise fastapi.HTTPException( status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                                     detail=f"Template with name '{source.name}' already exists. "
                                             "To update it use '/temlate/update' endpoint" )
    
    return json.dumps( dict() )

@app.post( path="/template/update" )
def update_template( source: TemplateBuildSources ) -> str:
    """"""
    if source.name == "" or source.name == None:
        raise fastapi.HTTPException( status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                                     detail="No name provided" )
    return json.dumps( dict() )

@app.post( path="/template/list" )
def list_templates( ) -> Metadata:
    pass