from django.test import TestCase
from features.models import Feature  

class FeatureModelTest(TestCase):
    def setUp(self):
        self.feature = Feature.objects.create(
            title="Test Feature",
            description="A test feature description",
        )

    def test_feature_creation(self):
        self.assertEqual(self.feature.title, "Test Feature")
        self.assertTrue(isinstance(self.feature, Feature))