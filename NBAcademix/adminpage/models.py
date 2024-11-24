from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

class StudentPerformance(models.Model):
    academic_year_in = models.CharField(max_length=50)  # e.g., FIRST, SECOND
    academic_year = models.CharField(max_length=20)  # e.g., 2023-2024
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['academic_year_in', 'academic_year']

    def __str__(self):
        return f"{self.academic_year_in} Year - {self.academic_year}"

class Document(models.Model):
    document = models.FileField(upload_to='documents/')
    original_filename = models.CharField(max_length=255, blank=True)  # New field
    uploaded_at = models.DateTimeField(auto_now_add=True)
    performance = models.ForeignKey(StudentPerformance, related_name='documents', on_delete=models.CASCADE)

    def __str__(self):
        return self.original_filename or os.path.basename(self.document.name)
