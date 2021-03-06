# Generated by Django 3.1.7 on 2021-03-09 09:05

import re
import base64

from django.db import migrations, models
import dtf.validators

try:
    from progressbar import progressbar
except:
    def progressbar(range):
        return range

float_pattern = re.compile('^[-+]?(?:(?:\d*\.\d+)|(?:\d+\.?))(?:[Ee][+-]?\d+)?$')
int_pattern = re.compile('^[-+]?\d+$')
base64_pattern = re.compile("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$")

def determine_valuetype(data):
    if int_pattern.match(data):
        return (int(data), 'integer')
    elif float_pattern.match(data):
        return (float(data), 'float')
    elif data.startswith("[") and data.endswith("]"):
        return (data, 'list')
    elif base64_pattern.match(data):
        data_bytes = bytes(data, 'ascii')
        if base64.b64encode(base64.b64decode(data_bytes)) == data_bytes:
            return (data, 'image')
    return (data, 'string')

def convert_to_valuetype(data, valuetype):
    if valuetype == 'integer':
        return int(data)
    elif valuetype == 'float':
        return float(data)
    return data

def upgrade_test_results(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    TestResult = apps.get_model('dtf', 'TestResult')

    def upgrade_results(test_results):
        new_test_results = []

        for item in test_results:

            value = item.get("value")
            valuetype = item.get("valuetype")
            if value is not None:
                if valuetype is None:
                    (value, valuetype) = determine_valuetype(value)
                else:
                    value = convert_to_valuetype(value, valuetype)
                value = {
                    "data": value,
                    "type": valuetype
                }
            else:
                value = None

            status = item.get("status")
            if status is None:
                status = "unknown"

            reference = item.get("reference")
            if reference is not None:
                (reference, valuetype) = determine_valuetype(reference)
                reference = {
                    "data": reference,
                    "type": valuetype
                }
            else:
                reference = None

            new_test_results.append({
                "name" : item["name"],
                "value": value,
                "status": status,
                "reference": reference,
            })
        return new_test_results

    for test_result in progressbar(TestResult.objects.using(db_alias).all().iterator()):
        test_result.results = upgrade_results(test_result.results)
        test_result.save()


def upgrade_test_references(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    TestReference = apps.get_model('dtf', 'TestReference')

    def upgrade_references(references):
        new_references = {}
        for (name, reference) in references.items():
            (data, datatype) = determine_valuetype(reference["value"])
            new_reference = {
                "value" : {
                    "data" : data,
                    "type" : datatype
                }
            }
            if 'ref_id' in reference:
                new_reference['source'] = int(reference['ref_id'])
            new_references[name] = new_reference
        return new_references

    for test_reference in progressbar(TestReference.objects.using(db_alias).all().iterator()):
        test_reference.references = upgrade_references(test_reference.references)
        test_reference.save()

class Migration(migrations.Migration):

    dependencies = [
        ('dtf', '0017_json_validators'),
    ]

    operations = [
        migrations.RunPython(upgrade_test_results, migrations.RunPython.noop),
        migrations.RunPython(upgrade_test_references, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='testreference',
            name='references',
            field=models.JSONField(default=dict, validators=[dtf.validators.JSONSchemaValidator(schema={'additionalProperties': {'additionalProperties': False, 'properties': {'source': {'type': 'integer'}, 'value': {'additionalProperties': False, 'allOf': [{'if': {'properties': {'type': {'const': 'integer'}}}, 'then': {'properties': {'data': {'type': 'integer'}}}}, {'if': {'properties': {'type': {'const': 'float'}}}, 'then': {'properties': {'data': {'type': 'number'}}}}, {'if': {'properties': {'type': {'const': 'string'}}}, 'then': {'properties': {'data': {'type': 'string'}}}}, {'if': {'properties': {'type': {'const': 'list'}}}, 'then': {'properties': {'data': {'type': 'string'}}}}, {'if': {'properties': {'type': {'const': 'image'}}}, 'then': {'properties': {'data': {'contentEncoding': 'base64', 'contentMediaType': 'image/png', 'type': 'string'}}}}], 'properties': {'data': {}, 'type': {'enum': ['integer', 'float', 'string', 'list', 'image'], 'type': 'string'}}, 'required': ['data', 'type'], 'type': 'object'}}, 'required': ['value'], 'type': 'object'}, 'schema': 'http://json-schema.org/draft-07/schema#', 'type': 'object'})]),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='results',
            field=models.JSONField(null=True, validators=[dtf.validators.JSONSchemaValidator(schema={'items': {'additionalProperties': False, 'properties': {'name': {'type': 'string'}, 'reference': {'oneOf': [{'additionalProperties': False, 'allOf': [{'if': {'properties': {'type': {'const': 'integer'}}}, 'then': {'properties': {'data': {'type': 'integer'}}}}, {'if': {'properties': {'type': {'const': 'float'}}}, 'then': {'properties': {'data': {'type': 'number'}}}}, {'if': {'properties': {'type': {'const': 'string'}}}, 'then': {'properties': {'data': {'type': 'string'}}}}, {'if': {'properties': {'type': {'const': 'list'}}}, 'then': {'properties': {'data': {'type': 'string'}}}}, {'if': {'properties': {'type': {'const': 'image'}}}, 'then': {'properties': {'data': {'contentEncoding': 'base64', 'contentMediaType': 'image/png', 'type': 'string'}}}}], 'properties': {'data': {}, 'type': {'enum': ['integer', 'float', 'string', 'list', 'image'], 'type': 'string'}}, 'required': ['data', 'type'], 'type': 'object'}, {'type': 'null'}]}, 'reference_source': {'type': 'integer'}, 'status': {'default': 'unknown', 'enum': ['skip', 'successful', 'unstable', 'unknown', 'failed', 'broken'], 'type': 'string'}, 'value': {'oneOf': [{'additionalProperties': False, 'allOf': [{'if': {'properties': {'type': {'const': 'integer'}}}, 'then': {'properties': {'data': {'type': 'integer'}}}}, {'if': {'properties': {'type': {'const': 'float'}}}, 'then': {'properties': {'data': {'type': 'number'}}}}, {'if': {'properties': {'type': {'const': 'string'}}}, 'then': {'properties': {'data': {'type': 'string'}}}}, {'if': {'properties': {'type': {'const': 'list'}}}, 'then': {'properties': {'data': {'type': 'string'}}}}, {'if': {'properties': {'type': {'const': 'image'}}}, 'then': {'properties': {'data': {'contentEncoding': 'base64', 'contentMediaType': 'image/png', 'type': 'string'}}}}], 'properties': {'data': {}, 'type': {'enum': ['integer', 'float', 'string', 'list', 'image'], 'type': 'string'}}, 'required': ['data', 'type'], 'type': 'object'}, {'type': 'null'}]}}, 'required': ['name', 'value'], 'type': 'object'}, 'schema': 'http://json-schema.org/draft-07/schema#', 'type': 'array'})]),
        ),
    ]
