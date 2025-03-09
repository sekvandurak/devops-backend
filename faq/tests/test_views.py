from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import Users
from faq.models import FAQ
from django.utils import timezone  # Import timezone

class FAQAPITest(APITestCase):
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
        self.faq_data = {
            "question": "What is this app?",
            "answer": "It's a great app!",
            "published": True,
            "created_at": timezone.now(),  # Use timezone.now() for timezone-aware datetime
        }
        self.faq = FAQ.objects.create(**self.faq_data)

    def test_create_faq(self):
        new_faq_data = {
            "question": "How does it work?",
            "answer": "Very well!",
            "published": False,
        }
        response = self.client.post('/api/faq/', new_faq_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FAQ.objects.count(), 2)
        self.assertEqual(response.data['question'], "How does it work?")
        self.assertFalse(response.data['published'])
        self.assertIn('created_at', response.data)  # Verify created_at is present
        self.assertIsNotNone(response.data['created_at'])

    def test_create_faq_unauthenticated(self):
        self.client.credentials()
        new_faq_data = {
            "question": "Unauthorized question?",
            "answer": "Should fail!",
            "published": True,
        }
        response = self.client.post('/api/faq/', new_faq_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_faq_list(self):
        response = self.client.get('/api/faq/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['question'], "What is this app?")

    def test_get_faq_detail(self):
        response = self.client.get(f'/api/faq/{self.faq.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['answer'], "It's a great app!")

    def test_update_faq(self):
        updated_data = {
            "question": "Updated question?",
            "answer": "Updated answer!",
            "published": False,
        }
        response = self.client.put(f'/api/faq/{self.faq.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.faq.refresh_from_db()
        self.assertEqual(self.faq.question, "Updated question?")
        self.assertEqual(self.faq.answer, "Updated answer!")
        self.assertFalse(self.faq.published)

    def test_delete_faq(self):
        response = self.client.delete(f'/api/faq/{self.faq.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FAQ.objects.count(), 0)