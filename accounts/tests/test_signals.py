from django.test import TestCase
from accounts.models import User, Profile


class UserSignalTestCase(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(
            email="test@test.com", password='1234')

    def test_post_save_user(self):
        self.assertTrue(Profile.objects.filter(user=self.test_user).exists())

    def test_valid_profile_username(self):

        self.assertEqual("test", self.test_user.profile.username)
