from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import TestMeasurement, TestResult

@receiver(post_save, sender=TestMeasurement)
def update_test_result_status_on_measurement_change(sender, instance, **kwargs):
    if not kwargs.get('raw', False) and instance.test_result:
        instance.test_result.downgrade_status()

@receiver(post_delete, sender=TestMeasurement)
def recalculate_test_result_status_after_measurement_delete(sender, instance, **kwargs):
    test_result = TestResult.objects.filter(pk=instance.test_result_id).first()
    if test_result is not None:
        test_result.recalculate_status()

@receiver(post_save, sender=TestResult)
@receiver(post_delete, sender=TestResult)
def update_submission_status_on_test_result_change(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        instance.downgrade_status()
