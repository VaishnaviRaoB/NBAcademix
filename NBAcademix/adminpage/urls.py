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
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)