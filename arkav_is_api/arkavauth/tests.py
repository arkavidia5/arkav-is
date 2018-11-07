from django.test import TestCase
from .models import User, RegistrationConfirmationAttempt, PasswordResetConfirmationAttempt


class RegistrationConfirmationAttemptTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(email="yonas@gmail.com")
        self.user2 = User.objects.create(email="adiel@gmail.com")

    def test_token_always_different(self):
        """
        Confirmation attempts should always have different tokens.
        """
        attempt1 = RegistrationConfirmationAttempt.objects.create(user=self.user1)
        attempt2 = RegistrationConfirmationAttempt.objects.create(user=self.user2)
        self.assertIsNotNone(attempt1.token)
        self.assertIsNotNone(attempt2.token)
        self.assertNotEqual(attempt1.token, attempt2.token)


class PasswordResetConfirmationAttemptTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(email="yonas@gmail.com")
        self.user2 = User.objects.create(email="adiel@gmail.com")

    def test_token_always_different(self):
        """
        Confirmation attempts should always have different tokens.
        """
        attempt1 = PasswordResetConfirmationAttempt.objects.create(user=self.user1)
        attempt2 = PasswordResetConfirmationAttempt.objects.create(user=self.user2)
        self.assertIsNotNone(attempt1.token)
        self.assertIsNotNone(attempt2.token)
        self.assertNotEqual(attempt1.token, attempt2.token)
