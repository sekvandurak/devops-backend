from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from contact.models import Contact
from users.models import Users  # Added import

class ContactAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Users.objects.create_user(
            name="John Doe",
            role="Admin",
            email="john@example.com",
            password="securepassword",
        )
        token_response = self.client.post('/api/token/', {
            "email": "john@example.com",
            "password": "securepassword",
        }, format='json')
        self.token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.contact_data = {
            "email": "contact@example.com",
            "name": "Jane Doe",
            "subject": "Support",
            "message": "Need help!",
        }
        self.contact = Contact.objects.create(**self.contact_data)

    def test_create_contact(self):
        new_contact_data = {
            "email": "new@example.com",
            "name": "John Smith",
            "subject": "Inquiry",
            "message": "Question about product",
        }
        response = self.client.post('/api/contact/', new_contact_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 2)

    def test_create_contact_unauthenticated(self):
        self.client.credentials()
        new_contact_data = {
            "email": "new2@example.com",
            "name": "John Smith",
            "subject": "Inquiry",
            "message": "Question about product",
        }
        response = self.client.post('/api/contact/', new_contact_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_contact_list(self):
        response = self.client.get('/api/contact/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_contact_detail(self):
        response = self.client.get(f'/api/contact/{self.contact.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], "contact@example.com")

    def test_update_contact(self):
        updated_data = {
            "email": "updated@example.com",
            "name": "Jane Doe",
            "subject": "Updated Support",
            "message": "Updated message",
        }
        response = self.client.put(f'/api/contact/{self.contact.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.email, "updated@example.com")

    def test_delete_contact(self):
        response = self.client.delete(f'/api/contact/{self.contact.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 0)