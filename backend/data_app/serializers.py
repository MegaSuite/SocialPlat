from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.hashers import make_password

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'job', 'contact', 'password', 'dob_year', 'dob_month', 'dob_day', 'gender', 'custom_gender', 'hobbies']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserProfileSerializer, self).create(validated_data)
