from django.contrib import admin

from .models import User, LocActivity


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'phone_number')
    list_display_links = ("id", "first_name", "phone_number")


@admin.register(LocActivity)
class LocActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'activity')
    list_display_links = ("id", "user")
