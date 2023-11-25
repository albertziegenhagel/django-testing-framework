"""
Contains all serializers needed for the API to transition between the json representation
and the database model of data
"""

import collections

from rest_framework import serializers

from django.contrib.auth.models import User

from dtf.models import Project, Membership, TestResult, ReferenceSet, TestReference, Submission, ProjectSubmissionProperty, Webhook, WebhookLogEntry
from dtf.functions import create_reference_query

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

def _try_build_absolute_uri(serializer, url):
    request = serializer.context.get('request')
    if request is not None:
        return request.build_absolute_uri(url)
    return url

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
                  'results',
                  'created',
                  'last_updated',
                  'submission',
                  'url',
                  'status']
        extra_kwargs = {'created': {'read_only': False, 'required':False}}

    def validate(self, data):
        # Default values in the 'results' JSON field have to be handled manually
        results = data.get('results', None)
        if not results:
            # if this is a partial update, that does not alter the results, we do not need to do anything
            # assert(self.partial)
            return data

        def get_current_reference(submission, test_name):
            reference_query = create_reference_query(submission.project, submission.info)
            reference_set = submission.project.reference_sets.filter(**reference_query).first()

            if reference_set is not None:
                return reference_set.test_references.filter(test_name=test_name).first()

            return None

        current_reference = None
        tried_get_reference = False

        for result in results:
            if not 'name' in result:
                continue # This is invalid and will be handled by the JSON schema validator

            # Set default status
            if not 'status' in result:
                result['status'] = 'unknown'

            # Set default reference
            if not 'reference' in result:
                # On the first missing reference, we try to find the current global reference for this test
                if current_reference is None and not tried_get_reference:
                    if self.partial:
                        # In a partial update, the submission and the name could either be modified
                        # (available in the 'data' field), or unmodified (use the current instance values)
                        submission = data.get('submission', self.instance.submission)
                        name = data.get('name', self.instance.name)
                        current_reference = get_current_reference(submission, name)
                    else:
                        current_reference = get_current_reference(data['submission'], data['name'])
                    tried_get_reference = True

                if current_reference is not None:
                    result['reference'] = current_reference.get_reference_or_none(result['name'])
                else:
                    result['reference'] = None
        return data

    def update(self, instance, validated_data):
        if 'results' in validated_data and self.partial:
            existing_results = instance.results.copy() if instance.results is not None else []

            existing_results_by_name = {}
            for i, result in enumerate(existing_results):
                existing_results_by_name[result['name']] = i

            for new_result in validated_data['results']:
                existing_result_index = existing_results_by_name.get(new_result['name'])
                if existing_result_index is None:
                    existing_results.append(new_result)
                else:
                    existing_results[existing_result_index].update(new_result)

            validated_data['results'] = existing_results

        return super().update(instance, validated_data)

    def get_url(self, obj):
        url = reverse('test_result_details', kwargs={'project_slug' : obj.submission.project.slug, 'test_id' : obj.pk})
        return _try_build_absolute_uri(self, url)

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
