from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import Users
import logging

class UsersAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "name": "John Doe",
            "role": "Admin",
            "email": "john@example.com",
            "password": "securepassword",
        }
        self.user = Users.objects.create_user(**self.user_data)
        # Get token
        token_response = self.client.post('/api/token/', {
            "email": "john@example.com",
            "password": "securepassword",
        }, format='json')
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_user(self):
        new_user_data = {
            "name": "Jane Doe",
            "role": "User",
            "email": "jane@example.com",
            "password": "anotherpassword",
        }
        response = self.client.post('/api/users/', new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Users.objects.count(), 2)
        self.assertEqual(response.data['name'], "Jane Doe")
        self.assertNotIn('password', response.data)

    def test_create_user_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        new_user_data = {
            "name": "Jane Doe",
            "role": "User",
            "email": "jane2@example.com",
            "password": "anotherpassword",
        }
        response = self.client.post('/api/users/', new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_list(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)  # Expect a list instead of paginated dict
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], "john@example.com")

    def test_get_user_detail(self):
        response = self.client.get(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "John Doe")



logger = logging.getLogger(__name__)

def test_update_user(self):
    updated_data = {
        "name": "John Smith",
        "role": "Admin",
        "email": "john@example.com",
        "password": "newpassword",  # Include password in update
    }
    response = self.client.put(f'/api/users/{self.user.id}/', updated_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.user.refresh_from_db()
    self.assertEqual(self.user.name, "John Smith")
    logger.info(f"User password hash: {self.user.password}")  # Debug the hash
    self.assertTrue(self.user.check_password("newpassword"))  # Verify new password

    def test_delete_user(self):
        response = self.client.delete(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Users.objects.count(), 0)