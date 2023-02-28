from django.db import models

class Chore(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    frequency = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    owner = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    photo_url = models.CharField(max_length=200)
    household = models.ForeignKey("Household", on_delete=models.CASCADE, null=True)
    status= models.BooleanField()
