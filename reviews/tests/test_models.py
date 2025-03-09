from django.test import TestCase
from users.models import Users
from reviews.models import Reviews

class ReviewsModelTest(TestCase):
    def setUp(self):
        self.user = Users.objects.create(
            name="John Doe",
            role="Admin",
            email="john@example.com",
            password="securepassword",
        )
        self.review = Reviews.objects.create(
            user=self.user,
            body="Great product!",
            stars=5,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.review), "Review by John Doe - 5 stars")

    def test_user_cascade_delete(self):
        self.user.delete()
        self.assertEqual(Reviews.objects.count(), 0)