from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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


class StudentBatch(models.Model):
    year = models.IntegerField()
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.year}"

class StudentDocument(models.Model):
    batch = models.ForeignKey(StudentBatch, on_delete=models.CASCADE)
    document = models.FileField(upload_to='student_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} - {self.batch}"
    
