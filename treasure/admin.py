from django.contrib import admin

from treasure.models import User


class UsersAdmin(admin.ModelAdmin):
    list_display = 'fullname', 'email', 'admin', 'contact', 'role', 'image', 'created', 'updated'


admin.register(User, UsersAdmin)
