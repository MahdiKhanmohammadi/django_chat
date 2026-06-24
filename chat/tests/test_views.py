from django.test import TestCase
from accounts.models import User
from django.urls import reverse_lazy


class ProfileUpdateViewTestCase(TestCase):
    def setUp(self):
        self.test_user = User(email='test@test.com')
        self.test_user.set_password("1234")
        self.test_user.save()
        self.path = reverse_lazy("chat:profile_update", kwargs={
                                 'username': self.test_user.generate_username()})

    def test_url_and_template(self):
        self.client.login(email=self.test_user.email, password="1234")

        response = self.client.get(
            f"/profile/{self.test_user.generate_username()}/update/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chat/profile_update.html")

    def test_revers_url_and_template(self):
        self.client.login(email=self.test_user.email, password="1234")

        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chat/profile_update.html")

    def test_with_anonymous_user(self):
        response = self.client.get("/profile/anonymous/update/")
        self.assertEqual(response.status_code, 302)

    def test_with_login_user_but_different_username(self):
        login_status = self.client.login(
            email="test@test.com", password="1234")
        self.assertTrue(login_status)

        response = self.client.get(reverse_lazy(
            "chat:profile_update", kwargs={'username': "invalid_username"}))

        self.assertEqual(response.status_code, 404)

    def test_view_for_update_object(self):
        login_status = self.client.login(
            email=self.test_user.email, password='1234')
        self.assertTrue(login_status)

        payload = {
            'first_name': 'test first name',
            'last_name': 'test last name',
        }

        response = self.client.post(self.path, data=payload)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('accounts:register'))

        self.test_user.profile.refresh_from_db()
        new_first_name = self.test_user.profile.first_name
        new_last_name = self.test_user.profile.last_name

        self.assertEqual("test first name", new_first_name)
        self.assertEqual("test last name", new_last_name)
