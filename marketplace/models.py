from django.db import models
from accounts.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.timesince import timesince
# Create your models here.

User = get_user_model()

class MarketplaceItem(models.Model):
    CATEGORY_CHOICES= (
        ('Crop','Crop'),
        ('Vegetables','Vegetables'),
        ('Fruits','Fruits'),
        ('Grains','Grains'),
        ('Seeds','Seeds'),
        ('Produce','Produce'),
    )

    user =  models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role':'farmer'}
    )
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=20,choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    quantity = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='marketplace/', blank=True, null=True)
    contact_phone = models.CharField(max_length=15,blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    unit = models.CharField(max_length=10, default='kg', help_text="e.g., kg, bunch, gram")
    updated_at = models.DateTimeField(auto_now=True)

    def time_since_posted(self):
        return timesince(self.created_at, timezone.now()) + " ago"
    def is_recent(self):
        return (timezone.now() - self.updated_at).total_seconds() < 86400  # 24 hrs
    def __str__(self):
        return self.name
