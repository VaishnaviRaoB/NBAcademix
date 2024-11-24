from django.contrib import admin
from .models import UserProfile,StudentPerformance,Document

admin.site.register([UserProfile,StudentPerformance,Document])
