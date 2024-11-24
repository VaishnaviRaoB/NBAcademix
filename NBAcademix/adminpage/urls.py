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
    path('student-details/', views.student_details_view, name='student_details'),
    path('student-performance/', views.student_performance_view, name='student_performance'),
    path('upload-performance-file/<int:performance_id>/', views.upload_performance_file, name='upload_performance_file'),
    path('upload-file/<int:batch_id>/', views.upload_file_view, name='upload_file_view'),
    path('download-performance-files/<int:performance_id>/', views.download_performance_files, name='download_performance_files'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)