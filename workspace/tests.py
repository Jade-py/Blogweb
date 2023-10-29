from django.test import TestCase, SimpleTestCase
from django.urls import reverse


class HomePageTest(SimpleTestCase):

    def test_WorkspacePage_url_existence(self):
        resp = self.client.get('/workspace/')
        self.assertEqual(resp.status_code, 200)

    def test_WorkspacePage_view_valid(self):
        resp = self.client.get(reverse('workspace'))
        self.assertEqual(resp.status_code, 200)

    def test_WorkspacePage_template_valid(self):
        resp = self.client.get(reverse('workspace'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'workspace.html')

# Create your tests here.
