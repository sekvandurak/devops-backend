from django.test import TestCase
from faq.models import FAQ  # Corrected from Faq

class FAQModelTest(TestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(
            question="Test Question",
            answer="Test Answer",
            published=True,
        )

    def test_faq_creation(self):
        self.assertEqual(self.faq.question, "Test Question")
        self.assertTrue(isinstance(self.faq, FAQ))