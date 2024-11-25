from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('homepage/', views.homepage, name='homepage'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('delete-account/', views.delete_account, name='delete_account'), 
    path('student-performance/', views.student_performance_view, name='student_performance'),
    path('upload-performance-file/<int:performance_id>/', views.upload_performance_file, name='upload_performance_file'),
    path('delete_performance/<int:performance_id>/', views.delete_performance, name='delete_performance'),
    path('delete_performance_file/<int:document_id>/', views.delete_performance_file, name='delete_performance_file'),
    path('download_performance_files/<int:performance_id>/', views.download_performance_files, name='download_performance_files'),
    path('student-list/', views.student_list_view, name='student_list'),
    path('delete-student-list/<int:list_id>/', views.delete_student_list, name='delete_student_list'),
    path('upload-student-file/<int:list_id>/', views.upload_student_file, name='upload_student_file'),
    path('download-student-files/<int:list_id>/', views.download_student_files, name='download_student_files'),
    path('delete-student-file/<int:document_id>/', views.delete_student_file, name='delete_student_file'),
    path('achievement/', views.achievement_view, name='achievement'),
path('delete-achievement/<int:achievement_id>/', views.delete_achievement, name='delete_achievement'),
path('upload-achievement-file/<int:achievement_id>/', views.upload_achievement_file, name='upload_achievement_file'),
path('download-achievement-files/<int:achievement_id>/', views.download_achievement_files, name='download_achievement_files'),
path('delete-achievement-file/<int:document_id>/', views.delete_achievement_file, name='delete_achievement_file'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
