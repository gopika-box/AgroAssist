from django.db import models
from accounts.models import User
from urllib.parse import urlparse, parse_qs


# Create your models here.
class Government_scheme(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    eligibility = models.TextField()
    deadline = models.DateField(
        blank=True,
        null=True
    )
    scheme_pdf = models.FileField(
        upload_to='scheme_pdfs/',
        blank=True,
        null=True
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'officer'}
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SchemeApplication(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    scheme = models.ForeignKey(Government_scheme, on_delete=models.CASCADE)
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")

    # Autofilled fields
    phone = models.CharField(max_length=15)
    panchayat = models.CharField(max_length=50)

    # Additional fields
    land_area = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    document = models.FileField(upload_to="scheme_applications/", blank=True, null=True)

    # Routing
    assigned_officer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assigned_scheme_applications"
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.farmer.username} - {self.scheme.title}"
    
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'officer'}
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    LESSON_TYPE = (
        ('video', 'Video'),
        ('notes', 'Notes'),
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )

    title = models.CharField(max_length=200)
    lesson_type = models.CharField(max_length=10, choices=LESSON_TYPE)

    video_url = models.URLField(blank=True, null=True)
    video_file = models.FileField(upload_to='lesson_videos/', blank=True, null=True)
    notes_file = models.FileField(upload_to='lesson_notes/', blank=True, null=True)

    description = models.TextField(blank=True)

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'officer'}
    )

    created_at = models.DateTimeField(auto_now_add=True)



    def save(self, *args, **kwargs):

        if self.video_url:

            url = self.video_url.strip()

            # ✅ Case 0: already embed link → clean it
            if "youtube.com/embed/" in url:
                video_id = url.split("/embed/")[-1].split("?")[0]
                self.video_url = f"https://www.youtube.com/embed/{video_id}"

            else:
                parsed = urlparse(url)

                # Case 1: watch?v=
                if "youtube.com" in parsed.netloc:
                    query = parse_qs(parsed.query)
                    video_id = query.get("v")

                    if video_id:
                        self.video_url = f"https://www.youtube.com/embed/{video_id[0]}"

                # Case 2: youtu.be/
                elif "youtu.be" in parsed.netloc:
                    video_id = parsed.path.strip("/")
                    self.video_url = f"https://www.youtube.com/embed/{video_id}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
  