from django.db import models


# Create your models here.


class List(models.Model):
    text = models.CharField(max_length=30, unique=True)



class Task(models.Model):
    text = models.TextField(max_length=250)
    list = models.ForeignKey(List, on_delete=models.CASCADE, default='1', verbose_name="Категория")

    class Meta:
        unique_together = ('text', 'list')
