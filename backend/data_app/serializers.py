from rest_framework import serializers
from .models import UserProfile, Comment, Post, FriendRequest, Friendship
from django.contrib.auth.hashers import make_password

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id', 'user_name', 'user_job', 'user_contact', 'user_password', 'user_dob_year', 'user_dob_month',
                  'user_dob_day', 'user_gender', 'user_custom_gender', 'user_hobbies', 'user_characters', 'avatar']
        extra_kwargs = {'user_password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['user_password'] = make_password(validated_data['user_password'])
        return super(UserProfileSerializer, self).create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    comment_author = serializers.CharField(source='comment_author.user_name', read_only=True)
    comment_author_id = serializers.IntegerField(source='comment_author.id', read_only=True)

    class Meta:
        model = Comment
        fields = ['comment_id', 'comment_content', 'comment_author_id', 'comment_author']

class PostSerializer(serializers.ModelSerializer):
    post_author = serializers.CharField(source='post_author.user_name', read_only=True)
    post_author_id = serializers.IntegerField(source='post_author.id', read_only=True)
    post_comments = CommentSerializer(many=True, read_only=True, source='comments')

    class Meta:
        model = Post
        fields = ['post_id', 'post_author_id', 'post_author', 'post_title', 'post_content', 'post_comments']


class FriendSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='friend.id')
    user_name = serializers.CharField(source='friend.user_name')
    user_job = serializers.CharField(source='friend.user_job')
    user_hobbies = serializers.JSONField(source='friend.user_hobbies')

    class Meta:
        model = Friendship
        fields = ['id', 'user_name', 'user_job', 'user_hobbies']

class FriendRequestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='from_user.id')
    name = serializers.CharField(source='from_user.user_name')
    friend_request_id = serializers.IntegerField(source='id')
    status = serializers.CharField()

    class Meta:
        model = FriendRequest
        fields = ['id', 'name', 'friend_request_id', 'status']


