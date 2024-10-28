from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    dob_year = models.IntegerField()
    dob_month = models.IntegerField()
    dob_day = models.IntegerField()
    gender = models.CharField(max_length=50)
    custom_gender = models.CharField(max_length=100, blank=True, null=True)
    hobbies = models.JSONField(default=list)

    USERNAME_FIELD = 'contact'

    def __str__(self):
        return self.name


