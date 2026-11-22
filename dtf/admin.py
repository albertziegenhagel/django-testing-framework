from django.contrib import admin

from dtf.models import Membership, Project, ProjectSubmissionProperty, TestResult, ReferenceSet, TestReference, TestReferenceMeasurement, Submission, Webhook

# Register your models here.

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    pass

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass

@admin.register(ProjectSubmissionProperty)
class ProjectSubmissionPropertyAdmin(admin.ModelAdmin):
    pass

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    pass

@admin.register(ReferenceSet)
class ReferenceSetAdmin(admin.ModelAdmin):
    pass

@admin.register(TestReference)
class TestReferenceAdmin(admin.ModelAdmin):
    pass

@admin.register(TestReferenceMeasurement)
class TestReferenceMeasurementAdmin(admin.ModelAdmin):
    list_display = ['name', 'test_reference', 'source']

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    pass

@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    pass