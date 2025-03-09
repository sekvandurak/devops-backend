from django.test import TestCase
from users.models import Users

class UsersModelTest(TestCase):
    def setUp(self):
        self.user = Users.objects.create_user(
            email="test@example.com",
            name="Test User",
            role="User",
            password="testpass123"
        )

    def test_password_hashing(self):
        self.assertTrue(self.user.check_password("testpass123"))  # Use check_password