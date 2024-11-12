# adminpage/models.py
from django.db import models
from django.contrib.auth.models import User

# adminpage/models.py
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=128, null=True, blank=True)  # Allow password to be null

    def __str__(self):
        return self.user.username
