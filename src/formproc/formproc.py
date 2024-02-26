from datetime import datetime
from io import BytesIO
from tempfile import NamedTemporaryFile
from re import match, compile, sub 
from asyncio import TaskGroup, create_task
from asyncio import run as aiorun


from openpyxl import load_workbook, Workbook
from openpyxl.worksheet.worksheet import Worksheet
from spire import xls
from spire.xls.common import PdfConformanceLevel, FileFormat


from ..routers import Languages

class FormProducer: 
    """A class to fill form template with data and produce form and jp-translated form"""
    def __init__( self,
                 template: bytes,
                 lang: Languages,
                 localizations: dict,
                 answer_data: dict ):
        self._locality_jp: dict = localizations[ Languages.Japanese ] 
        self._locality_target: dict = localizations[ lang ] 
        self._template: bytes = template
        self._answer_data: dict = answer_data
        self._jp_answer_data: dict = self._translate_jp( answer_data )
        return aiorun( self.create_filled_form_on_current_data )
        
    async def create_filled_form_on_current_data( self ):
        """A function to execute asynchronious parallel form"""
        with TaskGroup() as tg:
            jp_coro = tg.create_task( 
                coro = self.create_pdf_from_template( locality=self._locality_jp,
                                                      answers=self._answer_data )
            )
            local_coro = tg.create_task(
                coro = self.create_pdf_from_template( locality=self._locality_target,
                                                      answers=self._jp_answer_data  )
            )
        self.jp_doc = jp_coro.result()
        self.target_doc = local_coro.result()

    async def _translate_jp( self, data_to_translate: dict, lang: Languages ) -> dict:
        """A function  to translate answer data from presets to Japanese"""
        translation = {}
        pending_translation = {}
        for key in data_to_translate.keys():
            result = self._locality_jp.get( key, None )
            if result is not None:
                translation[ key ] = result
                continue
            pending_translation[ key ] = data_to_translate[ key ]
        translation.update( await self._translate_using_external_service( pending_translation ) )
        return translation

    async def _translate_using_external_service( self, data_to_translate: dict, lang: Languages ) -> dict:
        """A function to transalte incoming data to Japanese using external services """
        #TODO: 
        return data_to_translate
    
    async def create_pdf_from_template( self, locality: dict, answers: dict ) -> bytes:
        return await self._create_pdf( await self._fill( locality, answers ) )

    async def _create_pdf( self, wb: Workbook ) -> bytes:
        """Create PDF/A from Workbook"""
        openpxyl_wb_bytes = BytesIO()
        wb.save( openpxyl_wb_bytes )
        xls_wb = xls.Workbook()
        xls_wb.LoadFromStream( stream=openpxyl_wb_bytes.getvalue() )
        xls_wb.ConverterSetting.PdfConformanceLevel = PdfConformanceLevel.Pdf_A1A
        inmem_file = NamedTemporaryFile( )
        xls_wb.SaveToFile( inmem_file.name, FileFormat.PDF )
        return inmem_file.read()

    async def _fill( self, locality: dict, answers: dict ) -> Workbook:
        """A function to fill data in the workbook"""
        wb = load_workbook( filename=BytesIO( self._template ) )
        for sheet in wb:
            self._replace_placeholders_on_worksheet( sheet=sheet, locality=locality )
            self._fill_worksheet_by_index_value_dict( sheet=sheet, idx_value_dict=answers )


    def _replace_placeholders_on_worksheet( self, sheet: Worksheet, locality: dict ) -> None:
        """A function to replace placeholders {{key}}-marked with locality values"""
        placeholder_pattern = compile( r"{{*}}" )
        for row in sheet:
            for cell in row:
                key = match( placeholder_pattern, cell.value )
                cell.value = sub( placeholder_pattern, locality[ key ], cell.value )

    def _fill_worksheet_by_index_value_dict( self, sheet: Worksheet, idx_value_dict: dict ):
        """A function to fill answers data in worksheet according to indexes/values pair"""
        for idx, value in idx_value_dict.items():
            sheet[ idx ].value = value








