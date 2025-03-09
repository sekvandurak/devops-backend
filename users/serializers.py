from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'name', 'role', 'email', 'created_at', 'updated_at', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)  # Explicitly set the new password
            instance.save()  # Ensure the change is saved
        return instance