from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICE=(
        ('farmer','Farmer'),
        ('officer','Krishi Officer'),
        ('admin','Admin'),
    )

    role = models.CharField(max_length=20,choices=ROLE_CHOICE,default='farmer')
    is_approved = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.username} ({self.role})"

class OfficerProfile(models.Model):
    user= models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="officer_profile"
    )
    unique_id = models.CharField(max_length=50)
    panchayat= models.CharField(max_length=50)
    phone= models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username} - Officer"