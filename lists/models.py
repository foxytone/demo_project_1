from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.


class List(models.Model):
    text = models.CharField(max_length=60)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    
    class Meta:
        unique_together = ('text', 'user')


class Task(models.Model):
    text = models.TextField(max_length=250)
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)
    complited = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('text', 'list')


class Data(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_active_list = models.IntegerField(default=-1)
    lists_count = models.IntegerField(default=0)
