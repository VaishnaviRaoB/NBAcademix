from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from django.core.validators import FileExtensionValidator
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
    performance = models.ForeignKey(
        StudentPerformance, 
        related_name='documents', 
        on_delete=models.CASCADE
    )
    document = models.FileField(upload_to='performance_documents/')
    original_filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_filename
    
class StudentList(models.Model):
    batch_year = models.CharField(max_length=50)  # e.g., 2020-2024
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Batch Year - {self.batch_year}"
    
class StudentDocument(models.Model):
    document = models.FileField(upload_to='student_documents/')
    original_filename = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    student_list = models.ForeignKey(StudentList, related_name='documents', on_delete=models.CASCADE)

    def __str__(self):
        return self.original_filename or os.path.basename(self.document.name)
    
class Achievement(models.Model):
    event_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event - {self.event_name}"
    
class AchievementDocument(models.Model):
    document = models.FileField(upload_to='achievement_documents/')
    original_filename = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    achievement = models.ForeignKey(Achievement, related_name='documents', on_delete=models.CASCADE)

    def __str__(self):
        return self.original_filename or os.path.basename(self.document.name)
    

class PerformanceChart(models.Model):
    performance = models.OneToOneField(
        StudentPerformance,
        on_delete=models.CASCADE,
        related_name='performance_chart'
    )
    chart_image = models.TextField(null=True, blank=True)  # Base64 encoded image
    
    # Core metrics
    avg_cgpa = models.FloatField(null=True)
    total_students = models.IntegerField(default=0)
    total_cgpa = models.FloatField(null=True)
    detained_count = models.IntegerField(default=0)

    # Store semester-wise averages dynamically
    semester_averages = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Performance Chart - {self.performance.academic_year}"


class PassoutYear(models.Model):
    year = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return str(self.year)

class PlacementDetails(models.Model):
    name = models.CharField(max_length=100)
    usn = models.CharField(max_length=20)
    branch = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100)
    ctc = models.DecimalField(max_digits=10, decimal_places=2)
    other_details = models.TextField(blank=True, null=True)
    passout_year = models.ForeignKey(PassoutYear, on_delete=models.CASCADE, related_name='placement_details')
    offer_letter = models.FileField(upload_to='offer_letters/', null=True, blank=True)
    def __str__(self):
        return f"{self.name} - {self.company_name}"
    
class HigherStudy(models.Model):
    batch_year = models.CharField(max_length=9)  # e.g., 2013-2020
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Batch - {self.batch_year}"
    
class HigherStudyDocument(models.Model):
    document = models.FileField(upload_to='higher_study_documents/')
    original_filename = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    higher_study = models.ForeignKey(HigherStudy, related_name='documents', on_delete=models.CASCADE)

    def __str__(self):
        return self.original_filename or os.path.basename(self.document.name)