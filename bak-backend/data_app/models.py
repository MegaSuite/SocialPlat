from django.db import models

class DataEntry(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10)
    job = models.CharField(max_length=100)
    hobby = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

