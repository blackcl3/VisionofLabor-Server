from django.db import models

class User(models.Model):
    uid = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    household = models.ForeignKey("Household", on_delete=models.SET_NULL, null=True)
    photo_url = models.CharField(max_length=200)
    admin = models.BooleanField()

    @property
    def full_name(self):
        """Returns Full Name of User"""
        return f"{self.first_name} {self.last_name}"
