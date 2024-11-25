from django.contrib import admin
from .models import UserProfile,StudentPerformance,Document, StudentList, StudentDocument

admin.site.register([UserProfile,StudentPerformance,Document])
admin.site.register([StudentList, StudentDocument])

