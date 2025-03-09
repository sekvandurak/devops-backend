from django.test import TestCase
from contact.models import Contact

class ContactModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            email="contact@example.com",
            name="Jane Doe",
            subject="Support",
            message="Need help!",
        )

    def test_string_representation(self):
        self.assertEqual(str(self.contact), "Contact from Jane Doe")