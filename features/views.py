from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Features
from .serializers import FeaturesSerializer

class FeaturesViewSet(viewsets.ModelViewSet):
    queryset = Features.objects.all()
    serializer_class = FeaturesSerializer