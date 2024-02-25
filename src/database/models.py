from tortoise.models import Model
from tortoise import fields


class CategoryDBModel(Model):
    id = fields.IntField(pk=True)

    name = fields.CharField(max_length=100)

    class Meta:
        table = "categories"


class SectionDBModel(Model):
    id = fields.IntField(pk=True)

    name = fields.CharField(max_length=100)
    category = fields.ForeignKeyField('models.CategoryDBModel', related_name='section')

    class Meta:
        table = "sections"


class FormTemplateDBModel(Model):
    id = fields.IntField(pk=True)

    name = fields.CharField(max_length=200)
    excel_data = fields.data.BinaryField()
    markup_data = fields.data.JSONField()

    class Meta:
        table = "form_templates"


class FormMetadataDBModel(Model):
    id = fields.IntField(pk=True)

    description = fields.TextField()

    form = fields.ForeignKeyField('models.FormTemplateDBModel', related_name='form_metadata')
    category = fields.ForeignKeyField('models.CategoryDBModel', related_name='form_metadata')
    section = fields.ForeignKeyField('models.SectionDBModel', related_name='form_metadata')

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "form_metadata"


class LocalizationDBModel(Model):
    id = fields.IntField(pk=True)

    form = fields.ForeignKeyField('models.FormTemplateDBModel', related_name='form_localizations')
    name = fields.CharField(max_length=1000)
    lang = fields.CharField(max_length=10)
    value = fields.CharField(max_length=1000)

    class Meta:
        table = "form_localizations"


