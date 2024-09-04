from django.contrib import admin

from treasure.models import User


# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    list_display = 'fullname', 'email', 'admin', 'contact', 'role', 'image', 'created', 'updated'


admin.register(User, UsersAdmin)
