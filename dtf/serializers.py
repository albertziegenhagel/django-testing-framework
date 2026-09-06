"""
Contains all serializers needed for the API to transition between the json representation
and the database model of data
"""

import hashlib
import json

from rest_framework import serializers

from django.contrib.auth.models import User
from django.db import transaction

from dtf.models import Project, Membership, TestResult, ReferenceSet, TestReference, Submission, ProjectSubmissionProperty, Webhook, WebhookLogEntry, TestMeasurement, TestMeasurement, TestMeasurementImage, _value_json_schema_2
from dtf.functions import create_reference_query

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from dtf.validators import JSONSchemaValidator

def _try_build_absolute_uri(serializer, url):
    request = serializer.context.get('request')
    if request is not None:
        return request.build_absolute_uri(url)
    return url

def _get_or_create_test_measurement_image(data):
    md5sum = hashlib.md5(data.encode('utf-8')).hexdigest()
    image, _ = TestMeasurementImage.objects.get_or_create(
        md5sum=md5sum,
        defaults={'data': data},
    )
    if image.data != data:
        raise serializers.ValidationError('Image data hash collision.')
    return image

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class ProjectSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'slug', 'created', 'last_updated', 'url']
        extra_kwargs = {'created': {'read_only': False, 'required': False}}

    def get_url(self, obj):
        url = reverse('project_details', kwargs={'project_slug' : obj.slug})
        return _try_build_absolute_uri(self, url)

class MembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Membership
        fields = ['id', 'project', 'user', "role"]

    def to_internal_value(self, data):
        user_data = data.get('user')
        if isinstance(user_data, dict):
            user_data = UserSerializer(user_data).data
            data['user'] = user_data.get('id')
        self.fields['user'] = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
        return super().to_internal_value(data)

    def to_representation(self, value):
        if isinstance(self.fields['user'], serializers.PrimaryKeyRelatedField):
            self.fields['user'] = UserSerializer()
        return super().to_representation(value)

    def create(self, validated_data):
        return Membership.objects.create(**validated_data)

class ProjectSubmissionPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSubmissionProperty
        fields = ['project',
                  'id',
                  'name',
                  'required',
                  'display',
                  'display_replace',
                  'display_as_link',
                  'influence_reference']

class WebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webhook
        fields = ['project',
                  'id',
                  'name',
                  'url',
                  'secret_token',
                  'on_submission',
                  'on_test_result',
                  'on_reference_set',
                  'on_test_reference']

class ReferenceSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceSet
        fields = ['project',
                  'id',
                  'created',
                  'last_updated',
                  'property_values']
        extra_kwargs = {'created': {'read_only': False, 'required':False}}

class TestReferenceSerializer(serializers.ModelSerializer):
    default_source = serializers.PrimaryKeyRelatedField(queryset=TestResult.objects.all(), required=False)

    class Meta:
        model = TestReference
        fields = ['reference_set',
                  'test_name',
                  'default_source',
                  'id',
                  'created',
                  'last_updated',
                  'references']
        extra_kwargs = {'created': {'read_only': False, 'required':False}}

    def validate(self, data):
        if 'default_source' in data:
            default_source = data['default_source'].id
            del data['default_source']
        else:
            default_source = None

        reference_data = data['references']

        for parameter_name, parameter_values in reference_data.items():
            if not 'source' in parameter_values:
                if default_source is None:
                    raise serializers.ValidationError(\
                        "No test found with the given test id. Need a valid 'default_source' to properly set the reference")
                parameter_values['source'] = default_source

        return data

class TestResultSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = TestResult
        fields = ['name',
                  'id',
                  'created',
                  'last_updated',
                  'submission',
                  'url',
                  'status']
        extra_kwargs = {'created': {'read_only': False, 'required':False}}

    # def validate(self, data):
    #     # Default values in the 'results' JSON field have to be handled manually
    #     results = data.get('results', None)
    #     if not results:
    #         # if this is a partial update, that does not alter the results, we do not need to do anything
    #         # assert(self.partial)
    #         return data

    #     def get_current_reference(submission, test_name):
    #         reference_query = create_reference_query(submission.project, submission.info)
    #         reference_set = submission.project.reference_sets.filter(**reference_query).first()

    #         if reference_set is not None:
    #             return reference_set.test_references.filter(test_name=test_name).first()

    #         return None

    #     current_reference = None
    #     tried_get_reference = False

    #     for result in results:
    #         if not 'name' in result:
    #             continue # This is invalid and will be handled by the JSON schema validator

    #         # Set default status
    #         if not 'status' in result:
    #             result['status'] = 'unknown'

    #         # Set default reference
    #         if not 'reference' in result:
    #             # On the first missing reference, we try to find the current global reference for this test
    #             if current_reference is None and not tried_get_reference:
    #                 if self.partial:
    #                     # In a partial update, the submission and the name could either be modified
    #                     # (available in the 'data' field), or unmodified (use the current instance values)
    #                     submission = data.get('submission', self.instance.submission)
    #                     name = data.get('name', self.instance.name)
    #                     current_reference = get_current_reference(submission, name)
    #                 else:
    #                     current_reference = get_current_reference(data['submission'], data['name'])
    #                 tried_get_reference = True

    #             if current_reference is not None:
    #                 result['reference'] = current_reference.get_reference_or_none(result['name'])
    #             else:
    #                 result['reference'] = None
    #     return data

    # def update(self, instance, validated_data):
    #     if 'results' in validated_data and self.partial:
    #         existing_results = instance.results.copy() if instance.results is not None else []

    #         existing_results_by_name = {}
    #         for i, result in enumerate(existing_results):
    #             existing_results_by_name[result['name']] = i

    #         for new_result in validated_data['results']:
    #             existing_result_index = existing_results_by_name.get(new_result['name'])
    #             if existing_result_index is None:
    #                 existing_results.append(new_result)
    #             else:
    #                 existing_results[existing_result_index].update(new_result)

    #         validated_data['results'] = existing_results

    #     return super().update(instance, validated_data)

    def get_url(self, obj):
        url = reverse('test_result_details', kwargs={'project_slug' : obj.submission.project.slug, 'test_id' : obj.pk})
        return _try_build_absolute_uri(self, url)

class TestMeasurementValueField(serializers.Field):
    def to_representation(self, value):
        image = getattr(value, f'image_{self.field_name}')
        if image is not None:
            return {
                'type': 'image',
                'data': image.data
            }
        else:
            return getattr(value, f'data_{self.field_name}')

    def to_internal_value(self, data):
        if data is None:
            return {}
            # return {f'image_{self.field_name}' : 'null',
            #         f'data_{self.field_name}' : 'null'}
        if data['type'] == 'image':
            return {f'image_{self.field_name}' : data['data']}
        else:
            return {f'data_{self.field_name}' : data}

class StatusField(serializers.ChoiceField):
    _from_internal = {
        "SK": "skip",
        "SU": "successful",
        "US": "unstable",
        "UK": "unknown",
        "FA": "failed",
        "BR": "broken",
    }
    _to_internal = {
        "skip": "SK",
        "successful": "SU",
        "unstable": "US",
        "unknown": "UK",
        "failed": "FA",
        "broken": "BR",
    }
    _choices = {
        ("skip", "skip"),
        ("successful", "successful"),
        ("unstable", "unstable"),
        ("unknown", "unknown"),
        ("failed", "failed"),
        ("broken", "broken"),
    }

    def __init__(self, **kwargs):
        super().__init__(StatusField._choices, **kwargs)

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        return StatusField._to_internal.get(value, value)

    def to_representation(self, value):
        data = super().to_representation(value)
        return StatusField._from_internal.get(data, data)

class TestMeasurementSerializer(serializers.ModelSerializer):
    value     = TestMeasurementValueField(source='*', allow_null=True)
    reference = TestMeasurementValueField(source='*', required=False, allow_null=True)
    status    = StatusField(required=False)

    _data_value_validator=JSONSchemaValidator(schema=_value_json_schema_2)
    class Meta:
        model = TestMeasurement
        fields = ['name',
                  'id',
                  'test_result',
                  'status',
                  'value',
                  'reference',
                  'reference_source']

    def to_internal_value(self, data):
        result =  super().to_internal_value(data)
        return result

    def to_representation(self, value):
        result = super().to_representation(value)
        return result

    def validate(self, attrs):
        if 'image_value' in attrs:
            attrs['image_value'] = _get_or_create_test_measurement_image(
                attrs.pop('image_value')
            )
        if 'image_reference' in attrs:
            attrs['image_reference'] = _get_or_create_test_measurement_image(
                attrs.pop('image_reference')
            )
        if 'data_value' in attrs:
            TestMeasurementSerializer._data_value_validator(attrs.get('data_value'))
        if 'data_reference' in attrs:
            TestMeasurementSerializer._data_value_validator(attrs.get('data_reference'))
        return super().validate(attrs)

    # def create(self, validated_data):
    #     if 'image_value' in validated_data:
    #         validated_data['image_value'], _ = TestMeasurementImage.objects.get_or_create(data=validated_data.pop('image_value'))
    #     if 'image_reference' in validated_data:
    #         validated_data['image_reference'], _ = TestMeasurementImage.objects.get_or_create(data=validated_data.pop('image_reference'))
    #     return super().create(validated_data)

class TestResultCreateSerializer(TestResultSerializer):
    measurements = TestMeasurementSerializer(many=True, required=False)

    class Meta:
        model = TestResult
        fields = TestResultSerializer.Meta.fields + ['measurements']
        extra_kwargs = TestResultSerializer.Meta.extra_kwargs

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'measurements' in self.fields:
            self.fields['measurements'].child.fields['test_result'].read_only = True

    def create(self, validated_data):
        # Extract measurements data if present, default to empty list
        measurements_data = validated_data.pop('measurements', [])

        # Wrap in a transaction to guarantee data integrity
        with transaction.atomic():
            test_result = TestResult.objects.create(**validated_data)

            measurement_instances = [
                TestMeasurement(test_result=test_result, **measurement_data)
                for measurement_data in measurements_data
            ]
            TestMeasurement.objects.bulk_create(measurement_instances)

            if measurement_instances:
                test_result.downgrade_status()

        return test_result

    def to_internal_value(self, data):
        result =  super().to_internal_value(data)
        return result

    def to_representation(self, value):
        result = super().to_representation(value)
        return result

class SubmissionSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    class Meta:
        model = Submission
        fields = ['project',
                  'id',
                  'created',
                  'last_updated',
                  'info',
                  'url']
        read_only_fields = ['status']
        extra_kwargs = {'created': {'read_only': False, 'required':False}}

    def validate(self, data):
        info = data.get('info', None)
        project_properties = ProjectSubmissionProperty.objects.filter(project=data['project'], required=True)
        missing_property_names = []
        for prop in project_properties:
            if not info or not prop.name in info:
                missing_property_names.append(prop.name)

        if len(missing_property_names) > 0:
            missing_properties_str = ', '.join(missing_property_names)
            raise serializers.ValidationError(f"Missing required properties '{missing_properties_str}' in submission info")

        return data

    def get_url(self, obj):
        url = reverse('submission_details', kwargs={'project_slug' : obj.project.slug, 'submission_id' : obj.pk})
        return _try_build_absolute_uri(self, url)

class WebhookLogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookLogEntry
        fields = ['webhook',
            'created',
            'request_url', 'request_data', 'request_headers',
            'response_status', 'response_data', 'response_headers']
