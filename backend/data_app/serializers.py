from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.hashers import make_password

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id', 'user_name', 'user_job', 'user_contact', 'user_password', 'user_dob_year', 'user_dob_month',
                  'user_dob_day', 'user_gender', 'user_custom_gender', 'user_hobbies']
        extra_kwargs = {'user_password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['user_password'] = make_password(validated_data['user_password'])
        return super(UserProfileSerializer, self).create(validated_data)
