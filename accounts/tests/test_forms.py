from django.test import TestCase
from accounts.forms import RegisterUserModelForm
from accounts.models import User


class RegisterUserFormModelTestCase(TestCase):

    def setUp(self):

        self.test_user = User.objects.create(
            email="test@test.com", password=1234)

    def test_form_with_valid_data(self):
        form = RegisterUserModelForm(
            data={'email': 'newuser@gmail.com', 'password': '1234', 'confirm_password': '1234'})

        if form.errors:
            print(form.errors)

        self.assertTrue(form.is_valid())

    def test_clean_confirm_password_with_invalid_data(self):
        form = RegisterUserModelForm(
            data={'email': 'newuser@gmail.com', 'password': '1234', 'confirm_password': '123456'})

        self.assertFalse(form.is_valid())

    def test_form_with_repetitive_data(self):
        form = RegisterUserModelForm(data={"email": 'test@test.com',
                                           'password': '1234', 'confirm_password': '1234'})

        self.assertFalse(form.is_valid())
