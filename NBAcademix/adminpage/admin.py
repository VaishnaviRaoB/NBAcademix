from django.contrib import admin
from .models import UserProfile,StudentPerformance,Document, StudentList, StudentDocument,PerformanceChart,OfferLetter,PlacementDetails,PassoutYear,HigherStudy,HigherStudyDocument,Achievement,AchievementDocument

admin.site.register([UserProfile,StudentPerformance,Document,])
admin.site.register([StudentList, StudentDocument,PerformanceChart])
admin.site.register([PlacementDetails, OfferLetter, PassoutYear])
admin.site.register([HigherStudy,HigherStudyDocument])
admin.site.register([Achievement,AchievementDocument])
