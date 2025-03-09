from rest_framework import viewsets
from .models import FAQ  # Changed from Faq to FAQ
from .serializers import FAQSerializer

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer