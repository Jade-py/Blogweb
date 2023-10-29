from django.test import TestCase, SimpleTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your tests here.


def test_get_absolute_url(self):
    self.assertEqual(self.user.get_absolute_url(), '/testuser/')


class HomePageTest(SimpleTestCase):

    def test_homepage_url_existence(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_homepage_view_valid(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_homepage_template_valid(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'home.html')


class SignUpPageTest(TestCase):

    username = 'testuser'
    email = 'testuser@email.com'

    def test_SignUpPage_url_existence(self):
        resp = self.client.get('/signup/')
        self.assertEqual(resp.status_code, 200)

    def test_SignUpPage_view_valid(self):
        resp = self.client.get(reverse('signup'))
        self.assertEqual(resp.status_code, 200)

    def test_SignUpPage_template_valid(self):
        resp = self.client.get(reverse('signup'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'Signup.html')

    def test_SignUpFormPage(self):
        new_user = get_user_model().objects.create_user(
            self.username, self.email
        )
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
