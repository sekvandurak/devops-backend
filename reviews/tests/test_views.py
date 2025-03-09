from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import Users
from reviews.models import Reviews

class ReviewsAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Users.objects.create_user(
            name="John Doe",
            role="Admin",
            email="john@example.com",
            password="securepassword",
        )
        # Get token
        token_response = self.client.post('/api/token/', {
            "email": "john@example.com",
            "password": "securepassword",
        }, format='json')
        self.token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.review_data = {
            "user": self.user,
            "body": "Great product!",
            "stars": 5,
        }
        self.review = Reviews.objects.create(**self.review_data)

    def test_create_review(self):
        new_review_data = {
            "user": self.user.id,
            "body": "Amazing!",
            "stars": 4,
        }
        response = self.client.post('/api/reviews/', new_review_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reviews.objects.count(), 2)
        self.assertEqual(response.data['body'], "Amazing!")

    def test_get_review_list(self):
        response = self.client.get('/api/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_review_detail(self):
        response = self.client.get(f'/api/reviews/{self.review.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['body'], "Great product!")

    def test_update_review(self):
        updated_data = {
            "user": self.user.id,
            "body": "Updated review!",
            "stars": 3,
        }
        response = self.client.put(f'/api/reviews/{self.review.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.body, "Updated review!")

    def test_delete_review(self):
        response = self.client.delete(f'/api/reviews/{self.review.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Reviews.objects.count(), 0)