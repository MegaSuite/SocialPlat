from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class UserProfile(models.Model):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    user_name = models.CharField(max_length=100)
    user_job = models.CharField(max_length=100)
    user_contact = models.CharField(max_length=100)
    user_password = models.CharField(max_length=128)
    user_dob_year = models.IntegerField()
    user_dob_month = models.IntegerField()
    user_dob_day = models.IntegerField()
    user_gender = models.CharField(max_length=50)
    user_custom_gender = models.CharField(max_length=100, blank=True, null=True)
    user_hobbies = models.JSONField(default=list)
    user_characters = models.JSONField(default=list)
    user_like = models.JSONField(default=list)

    USERNAME_FIELD = 'user_contact'

    def __str__(self):
        return self.user_name


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts')
    post_title = models.CharField(max_length=200)
    post_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post_title

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment_author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.comment_author} on {self.post}"


class FriendRequest(models.Model):
    from_user = models.ForeignKey(UserProfile, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('refused', 'Refused')])

class Friendship(models.Model):
    user = models.ForeignKey(UserProfile, related_name='friendships', on_delete=models.CASCADE)
    friend = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
