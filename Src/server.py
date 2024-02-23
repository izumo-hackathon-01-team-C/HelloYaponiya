from typing import BinaryIO
import fastapi

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


app = fastapi.FastAPI()

# Interfaces
class FormTemplate( ABC ):
    """Abstract template for form processing"""
    @abstractmethod
    def fill( self, **kwargs ):
        """"A function to fill existing form with user's data stated in kwargs"""
        raise NotImplemented

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
    forms: list[ str ] = field( default_factory=list )    

@dataclass
class Section:
    """Adalos app's main screen section [e.g. Health, Taxes and so on]"""
    cathegories: list[ Cathegory ] = field( default_factory=list )

# Server globals
templates:      dict[ str, MarkedTemplate ]     = []
localizations:  dict[ str, Localization ]       = [] 
sections:       list[ Section ]                 = []
#TODO: recycling_bin for deleted objects?

# API Endpoints
@app.post( path="/template/create" )
def create_template( name: str,
                     markup_json: str, 
                     localization_json: str, 
                     metadata_json: str, 
                     template_xlsx_file: BinaryIO ) -> json:
    """A method to create template for form in Adalo/PythonServer"""
    global templates, localizations, sections

    if name in templates.keys(): 
        raise fastapi.HTTPException( status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                                     detail=f"Template with name '{name}' already exists. "
                                             "To update it use '/temlate/update' endpoint" )
    
    return json.dumps( dict() )

@app.post( path="/template/update" )
def update_template( name: str,
                     markup_json: str|None = None, 
                     localization_json: str|None = None, 
                     metadata_json: str|None = None, 
                     template_xlsx_file: BinaryIO|None = None ) -> json:
    """"""
    return json.dumps( dict() )
