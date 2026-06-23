from django.test import TestCase, Client
from django.urls import reverse_lazy
from accounts.models import Profile, User
from accounts.forms import RegisterUserModelForm


class RegisterUserFormViewTestCase(TestCase):
    def test_url_and_template(self):
        response = self.client.get('/account/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_reverse_url_name(self):
        response = self.client.get(reverse_lazy("accounts:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_view_with_valid_data(self):

        data = {
            "email": "newuser@gmail.com",
            "password": "1234",
            'confirm_password': "1234"
        }
        response = self.client.post(reverse_lazy(
            "accounts:register"), data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('accounts:login'))

        self.assertTrue(User.objects.filter(
            email='newuser@gmail.com').exists())

        self.assertTrue(Profile.objects.filter(username="newuser").exists())


class LoginUserFormViewTestCase(TestCase):

    def setUp(self):
        self.path = reverse_lazy("accounts:login")
        self.test_user = User(
            email="test@test.com", is_active=True)
        self.test_user.set_password("1234")
        self.test_user.save()

    def test_url_and_template(self):
        response = self.client.get("/account/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_reverse_url_name(self):
        response = self.client.get(reverse_lazy("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_view_with_valid_data(self):

        payload = {
            'email': 'test@test.com',
            'password': '1234'
        }

        response = self.client.post(self.path, data=payload, follow=True)

        self.assertEqual(response.status_code, 200)

        print(response.context.get('form').errors)

        user = response.context.get('user')

        self.assertTrue(user.is_authenticated)
