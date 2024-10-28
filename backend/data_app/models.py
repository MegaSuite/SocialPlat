from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    password = models.CharField(max_length=100)  # 注意：不要明文存储密码
    dob_year = models.IntegerField()
    dob_month = models.IntegerField()
    dob_day = models.IntegerField()
    gender = models.CharField(max_length=50)
    custom_gender = models.CharField(max_length=100, blank=True, null=True)
    hobbies = models.JSONField(default=list)

    def __str__(self):
        return self.name


