from django.db import models

class ChoreCategory(models.Model):

    chore = models.ForeignKey("Chore", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
