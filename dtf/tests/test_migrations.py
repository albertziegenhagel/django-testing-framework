from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase


class TestReferenceMeasurementMigrationTest(TransactionTestCase):
    migrate_from = ('dtf', '0026_testmeasurementimage_testmeasurement')
    migrate_to = ('dtf', '0027_testreferencemeasurement')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        executor = MigrationExecutor(connection)
        executor.migrate([cls.migrate_from])
        cls.old_apps = executor.loader.project_state([cls.migrate_from]).apps

    @classmethod
    def tearDownClass(cls):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDownClass()

    def test_existing_references_are_copied(self):
        Project = self.old_apps.get_model('dtf', 'Project')
        Submission = self.old_apps.get_model('dtf', 'Submission')
        TestResult = self.old_apps.get_model('dtf', 'TestResult')
        ReferenceSet = self.old_apps.get_model('dtf', 'ReferenceSet')
        TestReference = self.old_apps.get_model('dtf', 'TestReference')

        project = Project.objects.create(name='Migration project', slug='migration-project')
        submission = Submission.objects.create(project=project)
        source = TestResult.objects.create(name='Source test', submission=submission)
        reference_set = ReferenceSet.objects.create(project=project)
        test_reference = TestReference.objects.create(
            reference_set=reference_set,
            test_name='Reference test',
            references={
                'integer': {
                    'value': {'type': 'integer', 'data': 5},
                    'source': source.pk,
                },
                'null': {'value': None},
                'image': {
                    'value': {'type': 'image', 'data': 'aW1hZ2U='},
                    'source': 999999,
                },
            },
        )

        executor = MigrationExecutor(connection)
        executor.migrate([self.migrate_to])
        new_apps = executor.loader.project_state([self.migrate_to]).apps
        TestReferenceMeasurement = new_apps.get_model('dtf', 'TestReferenceMeasurement')
        measurements = {
            entry.name: entry
            for entry in TestReferenceMeasurement.objects.filter(test_reference_id=test_reference.pk)
        }

        self.assertEqual(measurements['integer'].data_value, {'type': 'integer', 'data': 5})
        self.assertEqual(measurements['integer'].source_id, source.pk)
        self.assertIsNone(measurements['null'].data_value)
        self.assertIsNone(measurements['null'].source_id)
        self.assertIsNone(measurements['image'].data_value)
        self.assertEqual(measurements['image'].image_value.data, 'aW1hZ2U=')
        self.assertIsNone(measurements['image'].source_id)

        executor = MigrationExecutor(connection)
        executor.migrate([self.migrate_from])
        restored_apps = executor.loader.project_state([self.migrate_from]).apps
        RestoredTestReference = restored_apps.get_model('dtf', 'TestReference')
        restored = RestoredTestReference.objects.get(pk=test_reference.pk)
        self.assertEqual(
            restored.references,
            {
                'integer': {
                    'value': {'type': 'integer', 'data': 5},
                    'source': source.pk,
                },
                'null': {'value': None},
                'image': {'value': {'type': 'image', 'data': 'aW1hZ2U='}},
            },
        )
