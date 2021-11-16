from django.db import models
from django.utils import timezone
# Create your models here.

class Contact(models.Model):
    fullname            = models.CharField(max_length=100)
    email               = models.EmailField()
    message             = models.TextField(max_length=300)
    timestamp           = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
