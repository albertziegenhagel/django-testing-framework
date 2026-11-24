import re

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from dtf.models import Project, Submission, TestResult


class TestResultNavigationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='navigation-test',
            email='navigation-test@example.com',
            password='password',
        )
        self.client.force_login(self.user)

        self.project = Project.objects.create(
            name='Navigation project',
            slug='navigation-project',
        )
        self.submissions = [
            Submission.objects.create(project=self.project)
            for _ in range(3)
        ]
        self.results = [
            TestResult.objects.create(submission=submission, name='Case')
            for submission in self.submissions
        ]
        self.results[1].status = 'successful'
        self.results[1].save(update_fields=['status'])
        self.submission_results = [self.results[1]]
        for name, status in (
            ('Earlier unsuccessful', 'failed'),
            ('Current successful', 'successful'),
            ('Later unsuccessful', 'broken'),
            ('Last successful', 'successful'),
        ):
            self.submission_results.append(TestResult.objects.create(
                submission=self.submissions[1],
                name=name,
                status=status,
            ))

        other_project = Project.objects.create(
            name='Other project',
            slug='other-project',
        )
        other_submission = Submission.objects.create(project=other_project)
        TestResult.objects.create(submission=other_submission, name='Case')
        other_name_submission = Submission.objects.create(project=self.project)
        TestResult.objects.create(submission=other_name_submission, name='Other case')

    def get_nav_control_attributes(self, response, control_id):
        links = re.findall(r'<a\b[^>]*>', response.content.decode())
        for link in links:
            attributes = dict(re.findall(r'([\w-]+)="([^"]*)"', link))
            if attributes.get('id') == control_id:
                return attributes
        self.fail(f'Navigation control {control_id!r} was not rendered')

    def assert_nav_control_links_to(self, response, control_id, test_result):
        attributes = self.get_nav_control_attributes(response, control_id)
        expected_url = reverse(
            'test_result_details',
            kwargs={
                'project_slug': self.project.slug,
                'test_id': test_result.pk,
            },
        )
        self.assertEqual(attributes.get('href'), expected_url)

    def assert_nav_control_disabled(self, response, control_id):
        attributes = self.get_nav_control_attributes(response, control_id)
        self.assertEqual(attributes.get('href'), '#')
        self.assertEqual(attributes.get('aria-disabled'), 'true')

    def test_navigation_is_scoped_and_query_count_is_bounded(self):
        with self.assertNumQueries(3):
            nav_data = self.project.get_nav_data(
                'Case',
                self.submissions[1].pk,
            )

        self.assertEqual(nav_data['previous'], self.results[0].pk)
        self.assertEqual(nav_data['next'], self.results[2].pk)
        self.assertEqual(nav_data['most_recent'], self.results[2].pk)

    def test_navigation_handles_first_and_latest_boundaries(self):
        first_nav_data = self.project.get_nav_data(
            'Case',
            self.submissions[0].pk,
        )
        latest_nav_data = self.project.get_nav_data(
            'Case',
            self.submissions[2].pk,
        )

        self.assertIsNone(first_nav_data['previous'])
        self.assertIsNotNone(first_nav_data['next'])
        self.assertIsNotNone(latest_nav_data['previous'])
        self.assertIsNone(latest_nav_data['next'])
        self.assertEqual(latest_nav_data['most_recent'], self.results[2].pk)

    def test_submission_navigation_is_ordered_and_skips_successful_tests(self):
        current_test = self.submission_results[2]
        with self.assertNumQueries(8):
            nav_data = current_test.get_submission_nav_data()

        self.assertEqual(nav_data, {
            'first': self.submission_results[0].pk,
            'previous': self.submission_results[1].pk,
            'next': self.submission_results[3].pk,
            'last': self.submission_results[4].pk,
            'first_not_successful': self.submission_results[1].pk,
            'previous_not_successful': self.submission_results[1].pk,
            'next_not_successful': self.submission_results[3].pk,
            'last_not_successful': self.submission_results[3].pk,
        })

        successful_submission = Submission.objects.create(project=self.project)
        only_successful_test = TestResult.objects.create(
            submission=successful_submission,
            name='Only successful test',
            status='successful',
        )
        nav_data = only_successful_test.get_submission_nav_data()
        self.assertIsNone(nav_data['first_not_successful'])
        self.assertIsNone(nav_data['last_not_successful'])

    def test_submission_navigation_controls_link_to_tests_in_current_submission(self):
        current_test = self.submission_results[2]
        response = self.client.get(reverse(
            'test_result_details',
            kwargs={
                'project_slug': self.project.slug,
                'test_id': current_test.pk,
            },
        ))

        self.assertEqual(response.status_code, 200)
        for control_id, target in (
            ('nav-first-in-submission', self.submission_results[0]),
            ('nav-previous-in-submission', self.submission_results[1]),
            ('nav-next-in-submission', self.submission_results[3]),
            ('nav-last-in-submission', self.submission_results[4]),
            ('nav-first-non-successful', self.submission_results[1]),
            ('nav-previous-non-successful', self.submission_results[1]),
            ('nav-next-non-successful', self.submission_results[3]),
            ('nav-last-non-successful', self.submission_results[3]),
        ):
            self.assert_nav_control_links_to(response, control_id, target)

    def test_submission_navigation_disables_first_and_last_boundaries(self):
        first_response = self.client.get(reverse(
            'test_result_details',
            kwargs={
                'project_slug': self.project.slug,
                'test_id': self.submission_results[0].pk,
            },
        ))
        self.assert_nav_control_disabled(first_response, 'nav-first-in-submission')
        self.assert_nav_control_disabled(first_response, 'nav-previous-in-submission')
        self.assert_nav_control_disabled(
            first_response,
            'nav-previous-non-successful',
        )

        last_response = self.client.get(reverse(
            'test_result_details',
            kwargs={
                'project_slug': self.project.slug,
                'test_id': self.submission_results[4].pk,
            },
        ))
        self.assert_nav_control_disabled(last_response, 'nav-last-in-submission')
        self.assert_nav_control_disabled(last_response, 'nav-next-in-submission')
        self.assert_nav_control_disabled(
            last_response,
            'nav-next-non-successful',
        )

        first_unsuccessful_response = self.client.get(reverse(
            'test_result_details',
            kwargs={
                'project_slug': self.project.slug,
                'test_id': self.submission_results[1].pk,
            },
        ))
        self.assert_nav_control_disabled(
            first_unsuccessful_response,
            'nav-first-non-successful',
        )

        last_unsuccessful_response = self.client.get(reverse(
            'test_result_details',
            kwargs={
                'project_slug': self.project.slug,
                'test_id': self.submission_results[3].pk,
            },
        ))
        self.assert_nav_control_disabled(
            last_unsuccessful_response,
            'nav-last-non-successful',
        )

    def test_navigation_controls_link_to_neighboring_test_results(self):
        response = self.client.get(reverse(
            'test_result_details',
            kwargs={
                'project_slug': self.project.slug,
                'test_id': self.results[1].pk,
            },
        ))

        self.assertEqual(response.status_code, 200)
        self.assert_nav_control_links_to(
            response,
            'nav-previous-submission',
            self.results[0],
        )
        self.assert_nav_control_links_to(
            response,
            'nav-next-submission',
            self.results[2],
        )
        self.assert_nav_control_links_to(
            response,
            'nav-latest-submission',
            self.results[2],
        )

    def test_navigation_controls_are_disabled_at_boundaries(self):
        response = self.client.get(reverse(
            'test_result_details',
            kwargs={
                'project_slug': self.project.slug,
                'test_id': self.results[0].pk,
            },
        ))

        self.assertEqual(response.status_code, 200)
        self.assert_nav_control_disabled(
            response,
            'nav-previous-submission',
        )

        response = self.client.get(reverse(
            'test_result_details',
            kwargs={
                'project_slug': self.project.slug,
                'test_id': self.results[2].pk,
            },
        ))

        self.assertEqual(response.status_code, 200)
        self.assert_nav_control_disabled(
            response,
            'nav-next-submission',
        )
        self.assert_nav_control_disabled(
            response,
            'nav-latest-submission',
        )
