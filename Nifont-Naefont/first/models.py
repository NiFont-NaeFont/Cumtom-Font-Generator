from django.db import models

# Create your models here.
class Construction(models.Model):
    name = models.CharField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


