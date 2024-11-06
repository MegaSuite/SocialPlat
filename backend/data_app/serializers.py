from rest_framework import serializers
from .models import UserProfile, Comment, Post
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


class CommentSerializer(serializers.ModelSerializer):
    comment_author = serializers.CharField(source='comment_author.user_name', read_only=True)

    class Meta:
        model = Comment
        fields = ['comment_id', 'comment_content', 'comment_author']

class PostSerializer(serializers.ModelSerializer):
    post_author = serializers.CharField(source='post_author.user_name', read_only=True)
    post_comments = CommentSerializer(many=True, read_only=True, source='comments')

    class Meta:
        model = Post
        fields = ['post_id', 'post_author', 'post_title', 'post_content', 'post_comments']