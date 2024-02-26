from ..database import FormTemplateDBModel, LocalizationDBModel
from ..routers import Languages

class FormProducer: 
    def __init__( self,
                 template: bytes,
                 markup: dict,
                 lang: Languages,
                 localizations: dict ) -> list[ bytes ]:
        pass