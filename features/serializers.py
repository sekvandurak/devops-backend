from rest_framework import serializers
from .models import Feature

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'title', 'description', 'created_at']