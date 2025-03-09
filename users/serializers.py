from rest_framework import serializers
from .models import Users


class UsersSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Users
        fields = '__all__'

#This serializer converts Users model instances to JSON and validates incoming data.
