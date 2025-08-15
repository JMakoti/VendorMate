from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class manageUser(AbstractUser):
    email = models.EmailField(unique=True,max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.company_name
