from django.db import models

# Create your models here.
class Crop(models.Model):
    SEASON_CHOICES = (
        ('Summer','Summer'),
        ('Monsoon','Monsoon'),
        ('Winter','Winter'),
        ('Spring','Spring'),
    )

    name = models.CharField(max_length=100,unique=True)
    season = models.CharField(max_length=20,choices=SEASON_CHOICES)
    soil_type = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)

    description = models.TextField()
    image = models.ImageField(upload_to='crop_images/', null=True, blank=True)


    def __str__(self):
        return self.name

class Fertilizer(models.Model):
    FERTILIZER_TYPE = (
        ('organic', 'Organic'),
        ('chemical', 'Chemical'),
        ('bio', 'Bio-fertilizer'),
    )

    name = models.CharField(max_length=100)      # Urea, DAP, Neem Cake
    brand = models.CharField(max_length=100)     # IFFCO, KRIBHCO, Local
    type = models.CharField(max_length=20, choices=FERTILIZER_TYPE)

    def __str__(self):
        return f"{self.name} ({self.brand})"

    
class CropFertilizerSchedule(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    fertilizer = models.ForeignKey(Fertilizer, on_delete=models.CASCADE)

    stage = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    notes = models.TextField()

    def __str__(self):
        return f"{self.crop.name} - {self.fertilizer.name}"

