from django.test import TestCase
from .models import User, EmailConfirmationAttempt


class EmailConfirmationAttemptTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(email="yonas@gmail.com")
        self.user2 = User.objects.create(email="adiel@gmail.com")

    def test_token_always_different(self):
        """Created EmailConfirmationAttempt always have different token"""
        attempt1 = EmailConfirmationAttempt.objects.create(user=self.user1)
        attempt2 = EmailConfirmationAttempt.objects.create(user=self.user2)
        self.assertIsNotNone(attempt1.token)
        self.assertIsNotNone(attempt2.token)
        self.assertNotEqual(attempt1.token, attempt2.token)

    def test_confirm(self):
        attempt1 = EmailConfirmationAttempt.objects.create(user=self.user1)
        user = User.objects.get(email=self.user1.email)
        self.assertTrue(user.email_confirmed)
        self.assertIsNotNone(attempt1.confirmed)
