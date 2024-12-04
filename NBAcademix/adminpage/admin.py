from django.contrib import admin
from .models import UserProfile,StudentPerformance,Document, StudentList, StudentDocument,PerformanceChart,PlacementDetails

admin.site.register([UserProfile,StudentPerformance,Document,])
admin.site.register([StudentList, StudentDocument,PerformanceChart])
admin.site.register([PlacementDetails])

