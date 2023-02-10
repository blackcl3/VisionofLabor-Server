from django.db import models

class Category(models.Model):
    value = models.AutoField(primary_key=True)
    label = models.CharField(max_length=50)
