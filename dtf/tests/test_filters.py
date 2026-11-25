
import django
import datetime

django.setup()

from django.test import TestCase
from django.utils import timezone

from dtf.models import Project, ReferenceSet, Submission, TestReference, TestReferenceMeasurement, TestResult
from dtf.templatetags.dtf.custom_filters import (
    as_measurement_entry,
    create_html_representation,
    local_datetime,
    reference_measurements_to_js_dict,
)

class ValueHtmlRepresentationTestCase(TestCase):

    def test_local_datetime_serializes_aware_value_as_iso8601(self):
        value = datetime.datetime(
            2026, 11, 24, 10, 9, 5,
            tzinfo=datetime.timezone(datetime.timedelta(hours=1)),
        )

        result = str(local_datetime(value))

        self.assertIn('datetime="2026-11-24T09:09:05Z"', result)
        self.assertIn('data-local-datetime="2026-11-24T09:09:05Z"', result)
        self.assertIn('title=', result)
        self.assertIn('<time ', result)

    def test_local_datetime_none_is_empty(self):
        self.assertEqual(local_datetime(None), "")

    def test_none(self):
        result = create_html_representation(None, None)
        self.assertEqual(result, "None")

    def test_integer(self):
        result = create_html_representation(123, 'integer')
        self.assertEqual(result, "123")

    def test_float(self):
        result = create_html_representation(1.23, 'float')
        self.assertEqual(result, "1.23")

        result = create_html_representation(1.234567891011121314e-9, 'float')
        self.assertEqual(result, "1.2345678910111213e-09")

    def test_float(self):
        result = create_html_representation(1.23, 'float')
        self.assertEqual(result, "1.23")

        result = create_html_representation(1.234567891011121314e-9, 'float')
        self.assertEqual(result, "1.2345678910111213e-09")

    def test_image(self):
        image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAVSURBVBhXY2BQ+/+fAQj+//9V8B8AJIUGjCXQWGcAAAAASUVORK5CYII="
        result = create_html_representation(image_base64, 'image')
        self.assertEqual(result, f"<img src='data:image/png;base64, {image_base64}' />")

    def test_duration(self):
        result = create_html_representation("P400DT3H5.5M", 'duration')
        self.assertEqual(result, f"400 days, 3:05:30")

        result = create_html_representation("PT1M1.23S", 'duration')
        self.assertEqual(result, f"0:01:01.230000")

        result = create_html_representation("PT0.4567S", 'duration')
        self.assertEqual(result, f"0:00:00.456700")

    def test_ndarray_vector(self):
        data = {
            "shape" : [ 2 ],
            "entries" : [
                { "data" : 1.0, "type" : "float" },
                { "data" : 2.0, "type" : "float" },
            ]
        }
        result = create_html_representation(data, 'ndarray')
        self.assertEqual(result,
         '<table class="ndarray-value">'
         '<tr><td>1.0</td></tr>'
         '<tr><td>2.0</td></tr>'
         '</table>')

    def test_ndarray_matrix(self):
        data = {
            "shape" : [ 2, 3 ],
            "entries" : [
                { "data" : 1.0, "type" : "float" },
                { "data" : 2.0, "type" : "float" },
                { "data" : 3.0, "type" : "float" },
                { "data" : 4.0, "type" : "float" },
                { "data" : 5.0, "type" : "float" },
                { "data" : 6.0, "type" : "float" },
            ]
        }
        result = create_html_representation(data, 'ndarray')
        self.assertEqual(result,
         '<table class="ndarray-value">'
         '<tr><td>1.0</td><td>2.0</td><td>3.0</td></tr>'
         '<tr><td>4.0</td><td>5.0</td><td>6.0</td></tr>'
         '</table>')

    def test_ndarray_tensor_3(self):
        data = {
            "shape" : [ 2, 2, 2 ],
            "entries" : [
                { "data" : 1.0, "type" : "float" },
                { "data" : 2.0, "type" : "float" },
                { "data" : 3.0, "type" : "float" },
                { "data" : 4.0, "type" : "float" },
                { "data" : 5.0, "type" : "float" },
                { "data" : 6.0, "type" : "float" },
                { "data" : 7.0, "type" : "float" },
                { "data" : 8.0, "type" : "float" },
            ]
        }
        result = create_html_representation(data, 'ndarray')
        self.assertEqual(result,
         '<table class="ndarray-value">'
         '<tr><td>1.0</td><td>2.0</td></tr>'
         '<tr><td>3.0</td><td>4.0</td></tr>'
         '</table>'
         '<table class="ndarray-value">'
         '<tr><td>5.0</td><td>6.0</td></tr>'
         '<tr><td>7.0</td><td>8.0</td></tr>'
         '</table>')

    def test_ndarray_tensor_4(self):
        data = {
            "shape" : [ 2, 2, 2, 2 ],
            "entries" : [
                { "data" : 1.0, "type" : "float" },
                { "data" : 2.0, "type" : "float" },
                { "data" : 3.0, "type" : "float" },
                { "data" : 4.0, "type" : "float" },
                { "data" : 5.0, "type" : "float" },
                { "data" : 6.0, "type" : "float" },
                { "data" : 7.0, "type" : "float" },
                { "data" : 8.0, "type" : "float" },
                { "data" : 9.0, "type" : "float" },
                { "data" : 10.0, "type" : "float" },
                { "data" : 11.0, "type" : "float" },
                { "data" : 12.0, "type" : "float" },
                { "data" : 13.0, "type" : "float" },
                { "data" : 14.0, "type" : "float" },
                { "data" : 15.0, "type" : "float" },
                { "data" : 16.0, "type" : "float" },
            ]
        }
        result = create_html_representation(data, 'ndarray')
        self.assertEqual(result,
        'Tensor-4 [2, 2, 2, 2]:'
         '<table class="ndarray-value">'
         '<tr><td>1.0</td></tr>'
         '<tr><td>2.0</td></tr>'
         '<tr><td>3.0</td></tr>'
         '<tr><td>4.0</td></tr>'
         '<tr><td>5.0</td></tr>'
         '<tr><td>6.0</td></tr>'
         '<tr><td>7.0</td></tr>'
         '<tr><td>8.0</td></tr>'
         '<tr><td>9.0</td></tr>'
         '<tr><td>10.0</td></tr>'
         '<tr><td>11.0</td></tr>'
         '<tr><td>12.0</td></tr>'
         '<tr><td>13.0</td></tr>'
         '<tr><td>14.0</td></tr>'
         '<tr><td>15.0</td></tr>'
         '<tr><td>16.0</td></tr>'
         '</table>')

    def test_ndarray_invalid(self):
        data = {
            "shape" : [ 2, 3 ],
            "entries" : [
                { "data" : 1.0, "type" : "float" },
                { "data" : 2.0, "type" : "float" },
                { "data" : 3.0, "type" : "float" },
                { "data" : 4.0, "type" : "float" },
                # Missing two values
            ]
        }
        result = create_html_representation(data, 'ndarray')
        self.assertEqual(result,
        'Tensor-2 [2, 3]:'
         '<table class="ndarray-value">'
         '<tr><td>1.0</td></tr>'
         '<tr><td>2.0</td></tr>'
         '<tr><td>3.0</td></tr>'
         '<tr><td>4.0</td></tr>'
         '</table>')

    def test_list(self):
        result = create_html_representation(str([1.0, 2.0, 3.0]), 'list')
        result = "".join(result.split()) # remove all whitespace
        self.assertEqual(result, "1.0<br>2.0<br>3.0")


class ReferenceMeasurementFilterTestCase(TestCase):
    def setUp(self):
        project = Project.objects.create(name='Test project', slug='test-project')
        submission = Submission.objects.create(project=project)
        self.source = TestResult.objects.create(name='Test', submission=submission)
        reference_set = ReferenceSet.objects.create(project=project)
        test_reference = TestReference.objects.create(
            reference_set=reference_set,
            test_name='Test',
        )
        self.measurement = TestReferenceMeasurement.objects.create(
            test_reference=test_reference,
            name='Result',
            data_value={'type': 'integer', 'data': 7},
            source=self.source,
        )
        self.project = project

    def test_reference_measurements_to_js_dict(self):
        import json

        result = json.loads(reference_measurements_to_js_dict(
            self.measurement.test_reference.measurements
        ))
        self.assertEqual(
            result,
            {
                'Result': {
                    'value': {'type': 'integer', 'data': 7},
                    'source': self.source.pk,
                }
            },
        )

    def test_as_measurement_entry(self):
        result = as_measurement_entry(self.measurement, self.project)
        self.assertIn(f"href='/{self.project.slug}/tests/{self.source.pk}'", result)
        self.assertIn('>7</a>', result)
