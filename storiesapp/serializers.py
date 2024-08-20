from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .models import User,Story

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)

class StorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Story
        fields = ['id', 'title', 'contributions', 'created_by','image']
        read_only_fields = ['created_by']
    
    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:  
            raise ValidationError("Image file too large ( > 2MB )")
        if value.image.format not in ['JPEG', 'PNG']:
            raise ValidationError("Image format not supported")
        return value
