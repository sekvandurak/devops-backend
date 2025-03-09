from rest_framework import viewsets
from .models import Feature  # Import from models, not self-referential
from .serializers import FeatureSerializer

class FeaturesViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer