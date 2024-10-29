from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class UserProfile(models.Model):
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

    USERNAME_FIELD = 'user_contact'

    def __str__(self):
        return self.user_name


