from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path("admin_home/", views.admin_home, name="admin_home"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),  
    path("students/", views.students, name="students"),
]
