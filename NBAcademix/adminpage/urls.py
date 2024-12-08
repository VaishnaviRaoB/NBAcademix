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
    path('generate-performance-chart/<int:document_id>/', views.generate_performance_chart, name='generate_performance_chart'),
    path('download-performance-chart/<int:performance_id>/', views.download_performance_chart, name='download_performance_chart'),
    path('placement/', views.placement_home, name='placement_home'),
    path('placement/year/<int:year_id>/', views.placement_year_details, name='placement_year_details'),
    path('placement/add/<int:year_id>/', views.add_placement_details, name='add_placement_details'),
    path('upload_offer_letter/<int:placement_id>/', views.upload_offer_letter, name='upload_offer_letter'),
    path('delete_passout_year/<int:year_id>/', views.delete_passout_year, name='delete_passout_year')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
