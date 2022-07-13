from django.db import models


# Create your models here.

class Users(models.Model):
    """User DataBase Model"""
    phone = models.CharField(max_length=50, blank=True, null=True)
    user_name = models.CharField(max_length=200, null=True)
    user_id = models.IntegerField(unique=True)
