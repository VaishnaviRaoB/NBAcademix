# adminpage/admin.py
from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_username', 'password', 'created_at')  # Display username, password, and signup date

    # Method to display the username from the User model
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

admin.site.register(UserProfile, UserProfileAdmin)
