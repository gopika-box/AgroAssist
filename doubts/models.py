from django.db import models
from django.conf import settings
from accounts.models import FarmerProfile, OfficerProfile  # adjust if needed

class Doubt(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Replied', 'Replied'),
    ]

    farmer = models.ForeignKey(
        FarmerProfile,
        on_delete=models.CASCADE
    )

    officer = models.ForeignKey(
        OfficerProfile,
        on_delete=models.CASCADE
    )

    panchayat = models.CharField(max_length=50)

    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='doubts/', blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
