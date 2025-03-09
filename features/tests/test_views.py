from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import Users
from features.models import Feature

class FeaturesAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Users.objects.create_user(
            name="John Doe",
            role="Admin",
            email="john@example.com",
            password="securepassword",
        )
        # Get JWT token
        token_response = self.client.post('/api/token/', {
            "email": "john@example.com",
            "password": "securepassword",
        }, format='json')
        self.token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.feature_data = {
            "title": "New Feature",
            "description": "A great new addition!",
        }
        self.feature = Feature.objects.create(**self.feature_data)

    def test_create_feature(self):
        new_feature_data = {
            "title": "Another Feature",
            "description": "Another great addition!",
        }
        response = self.client.post('/api/features/', new_feature_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feature.objects.count(), 2)

    def test_create_feature_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        new_feature_data = {
            "title": "Unauthorized Feature",
            "description": "Should fail!",
        }
        response = self.client.post('/api/features/', new_feature_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_feature_list(self):
        response = self.client.get('/api/features/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_feature_detail(self):
        response = self.client.get(f'/api/features/{self.feature.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "New Feature")

    def test_update_feature(self):
        updated_data = {
            "title": "Updated Feature",
            "description": "Updated description!",
        }
        response = self.client.put(f'/api/features/{self.feature.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.feature.refresh_from_db()
        self.assertEqual(self.feature.title, "Updated Feature")

    def test_delete_feature(self):
        response = self.client.delete(f'/api/features/{self.feature.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Feature.objects.count(), 0)