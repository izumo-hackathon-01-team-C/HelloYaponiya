from datetime import datetime
from os import getenv

import subprocess
from io import BytesIO
from tempfile import NamedTemporaryFile, TemporaryDirectory

from re import match, compile, sub, search 
from pathlib import Path

from asyncio import TaskGroup, create_task, get_event_loop
from asyncio import run as aiorun


from openpyxl import load_workbook 
from openpyxl import Workbook as OpxlWorkbook
from openpyxl.worksheet.worksheet import Worksheet

from ..models.enums import LanguageEnum 
from ..translation_api.client import TranslationClient

class FormProducer: 
    """A class to fill form template with data and produce form and jp-translated form"""
    def __init__( self,
                 template: bytes,
                 lang: LanguageEnum,
                 localizations: dict,
                 answer_data: dict ):
        self._lang = lang
        self._locality_jp: dict = localizations[ LanguageEnum.JAPANESE ] 
        self._locality_target: dict = localizations[ lang ] 
        self._template: bytes = template
        self._answer_data: dict = answer_data
        self._replace_bools_with_checkboxes( self._answer_data )

    def _replace_bools_with_checkboxes( self, answer_data: dict ):
        for key, value in answer_data.items():
            if isinstance( value, bool ):
                answer_data[ key ] = "■" if value else "☐" 

    async def execute(self):
        self._jp_answer_data: dict = await self._translate_jp( self._answer_data ) 
        return await self.create_filled_form_on_current_data()
        
    async def create_filled_form_on_current_data( self ):
        """A function to execute asynchronious parallel form"""
        async with TaskGroup() as tg:
            jp_coro = tg.create_task( 
                coro = self.create_pdf_from_template( locality=self._locality_jp,
                                                      answers=self._jp_answer_data )
            )
            # local_coro = tg.create_task(
            #     coro = self.create_pdf_from_template( locality=self._locality_target,
            #                                           answers=self._jp_answer_data  )
            # )
        self.jp_doc = jp_coro.result()
        #self.target_doc = local_coro.result()

    async def _translate_jp( self, data_to_translate: dict) -> dict:
        """A function  to translate answer data from presets to Japanese"""
        translation = {}
        pending_translation = {}
        for key in data_to_translate.keys():
            result = self._locality_jp.get( key, None )
            if result is not None:
                translation[ key ] = result
                continue
            pending_translation[ key ] = data_to_translate[ key ]
        translation.update( await self._translate_using_external_service( pending_translation, self._lang, LanguageEnum.JAPANESE ) )
        return translation

    async def _translate_using_external_service( self, data_to_translate: dict, source_lang: LanguageEnum, target_lang: LanguageEnum ) -> dict:
        """A function to transalte incoming data to Japanese using external services """
        apikey = getenv( "GOOGLE_API" )
        tr = TranslationClient( apikey )
        return await tr.translate_key_value_dict(
            data=data_to_translate,
            from_lang=source_lang,
            to_lang=target_lang
        )
    
    async def create_pdf_from_template( self, locality: dict, answers: dict ) -> bytes:
        return await self._create_pdf( await self._fill( locality, answers ) )

    async def _create_pdf( self, wb: OpxlWorkbook ) -> bytes:
        """Create PDF/A from Workbook"""
        #TODO: Move write to asyncio 
        in_inmem_file = NamedTemporaryFile( )
        wb.save( in_inmem_file.name )
        return self.convert_pdf_libreoffice( source_file=in_inmem_file )
    
    def convert_pdf_libreoffice( self, source_file: NamedTemporaryFile ) -> bytes:
        with TemporaryDirectory() as out_dir:
            #dev_null = open(os.devnull, 'w')
            subprocess.run( ['libreoffice',
                                '--headless',
                                "--nologo",
                                "--nofirststartwizard",
                                '--convert-to',
                                'pdf',
                                '--outdir',
                                out_dir,
                                source_file.name ], )
                             #stderr=dev_null,
                             #stdout=dev_null )
            #dev_null.close()
            files = Path( out_dir ).glob('*.pdf')
            with open( list( files )[ 0 ], "rb" ) as src:
                return src.read()


    async def _fill( self, locality: dict, answers: dict ) -> OpxlWorkbook:
        """A function to fill data in the workbook"""
        wb = load_workbook( filename=BytesIO( self._template ) )
        for sheet in wb:
            self._replace_placeholders_on_worksheet( sheet=sheet, locality=locality )
            self._fill_worksheet_by_index_value_dict( sheet=sheet, idx_value_dict=answers )
        return wb


    def _replace_placeholders_on_worksheet( self, sheet: Worksheet, locality: dict ) -> None:
        """A function to replace placeholders {{key}}-marked with locality values"""
        placeholder_pattern = compile( r"{{.*}}" )
        for row in sheet:
            for cell in row:
                if cell.value is None or r"{{" not in cell.value:
                    continue 
                key = search( placeholder_pattern, cell.value ).string
                if key is None:
                    continue
                key = sub( r"^.*{{", "", key)
                key = sub( r"}}.*", "", key)
                cell.value = sub( placeholder_pattern, locality[ key ], cell.value )

    def _fill_worksheet_by_index_value_dict( self, sheet: Worksheet, idx_value_dict: dict ):
        """A function to fill answers data in worksheet according to indexes/values pair"""
        for idx, value in idx_value_dict.items():
            sheet[ idx ].value = value








