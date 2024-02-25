from tortoise.models import Model
from tortoise import fields


class CategoryDBModel(Model):
    id = fields.IntField(pk=True)

    name = fields.CharField(max_length=100)


class SectionDBModel(Model):
    id = fields.IntField(pk=True)

    name = fields.CharField(max_length=100)
    category_id = fields.ForeignKeyField('CategoryDBModel', related_name='section')


class FormTemplateDBModel(Model):
    id = fields.IntField(pk=True)

    name = fields.CharField(max_length=200)
    description = fields.TextField()
    excel_data = fields.data.BinaryField()
    markup_data = fields.data.JSONField()


class FormMetadataDBModel(Model):
    id = fields.IntField(pk=True)

    form_id = fields.ForeignKeyField('FormTemplatesDBModel', related_name='form_metadata')
    category_id = fields.ForeignKeyField('CategoryDBModel', related_name='form_metadata')
    section_id = fields.ForeignKeyField('SectionDBModel', related_name='form_metadata')

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class LocalizationDBModel(Model):
    id = fields.IntField(pk=True)

    form_id = fields.ForeignKeyField('FormDBModel', related_name='form_localizations')
    name = fields.CharField(max_length=1000)
    lang = fields.CharField(max_length=10)
    value = fields.CharField(max_length=1000)


