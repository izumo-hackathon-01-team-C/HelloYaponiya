import json
from functools import cache

import fastapi
from fastapi import Request, UploadFile
from fastapi.routing import APIRouter
from fastapi.responses import StreamingResponse

from pydantic import BaseModel, model_validator

from tortoise.exceptions import DoesNotExist, MultipleObjectsReturned, OperationalError
from tortoise.transactions import in_transaction

from src.database.models import FormTemplateDBModel, FormMetadataDBModel, LocalizationDBModel
from src.models.enums import LanguageEnum


router = APIRouter()

# ================================================== #
# ================= API's models ================= #
# ================================================== #


class MetadataForm(BaseModel):
    """Metadata for versioning and organizing structure"""
    name: str
    description: str
    # category: str
    # section: str
    # creation_datetime: datetime
    # update_datetime: datetime


class TemplateBuildSourcesForm(BaseModel):
    """Data for building documents templates and storing them in app's structure"""
    metadata: MetadataForm

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class TemplateFillerData(BaseModel):
    """Data for filling form template"""
    lang: LanguageEnum
    json_data: str


class FillUpResult(BaseModel):
    lang: LanguageEnum
    japanese: bytes
    local: bytes


class CreateTemplateResult(BaseModel):
    template_id: str
    metadata_id: str
    total_locales: int


# ================================================== #
# ================= API's endpoint ================= #
# ================================================== #


# @router.post(path="/template/create", response_model=CreateTemplateResult)
# async def create_template(
#         excel_data: UploadFile,
#         markup_data: UploadFile,
#         localization_data: UploadFile,
#         source: TemplateBuildSourcesForm,
#
# ) -> CreateTemplateResult:
#     """A method to create template for form in Adalo/PythonServer"""
#     try:
#         await FormTemplateDBModel.get(name=source.metadata.name)
#
#         raise fastapi.HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST,
#                                     detail=f"Template with name '{source.metadata.name}' already exists. "
#                                            "To update it use '/temlate/update' endpoint")
#     except MultipleObjectsReturned:
#         raise fastapi.HTTPException(
#             status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Incorrect state"
#         )
#     except DoesNotExist:
#         pass
#
#     try:
#         async with in_transaction():
#             template_model = await FormTemplateDBModel.create(
#                 name=source.metadata.name,
#                 excel_data=excel_data.file.read(),
#                 markup_data=json.loads(markup_data.file.read())
#             )
#             metadata = await FormMetadataDBModel.create(
#                 description=source.metadata.description,
#                 template=template_model
#             )
#             localization_json = json.loads(localization_data.file.read())
#             localization_db_list = []
#             for lang, data in localization_json.items():
#                 for key, value in data.items():
#                     localization_db_list.append(
#                         LocalizationDBModel(
#                             template=template_model,
#                             lang=lang,
#                             key=key,
#                             value=value
#                         )
#                     )
#             await LocalizationDBModel.bulk_create(localization_db_list)
#
#     except OperationalError:
#         raise fastapi.HTTPException(
#             status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail='Something went wrong'
#         )
#
#     return CreateTemplateResult(
#         template_id=str(template_model.id),
#         metadata_id=str(metadata.id),
#         total_locales=len(localization_db_list)
#     )
#
#
# @router.post(path="/template/update")
# async def update_template(
#         request: Request,
#         source: TemplateBuildSourcesForm,
#         excel_data: UploadFile,
#         markup_data: UploadFile
# ) -> CreateTemplateResult:
#     """"""
#
#     if source.name == "":
#         raise fastapi.HTTPException(
#             status_code=fastapi.status.HTTP_400_BAD_REQUEST,
#             detail="No name provided"
#         )
#
#     try:
#         existing_model = await FormTemplateDBModel.get(
#             name=source.metadata.name
#         )
#     except DoesNotExist:
#         raise fastapi.HTTPException(
#             status_code=fastapi.status.HTTP_404_NOT_FOUND,
#         )
#
#     existing_model.excel_data = excel_data
#     existing_model.markup_data = markup_data
#     existing_model.name = source.name
#     existing_model.description = source.description
#     existing_model.localization_json = source.localization_json
#     existing_model.metadata_json = source.metadata_json
#
#     await existing_model.save()
#
#     return CreateTemplateResult(
#         id=existing_model.id
#     )


@router.get(path="/template/fill_up/{form_name}")
def fill_up(form_name: str, answer: dict[str, str]) -> StreamingResponse:
    return StreamingResponse(b'123', media_type="application/pdf")


@router.get(path='/template/markup/{markup_name}')
async def get_markup(request: Request, markup_name: str) -> list:
    if markup := request.app.state.file_manager.get_file_by_form_name(
        form_name=markup_name, file_type='markup'
    ):
        return json.loads(markup)
    else:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail='Markup not found'
        )
