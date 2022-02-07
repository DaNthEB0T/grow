from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import GrowUser

class GrowUserAdminConfig(UserAdmin):
    search_fields = ("email", "username")
    list_display = ("email", "username", "is_validated", "is_staff", "is_creator", "is_active")
    list_filter = ("is_active", "is_staff", "is_creator")
    ordering = ("username",)
    
    fieldsets = (
        (None, {'fields': ("email", "username")}),
        ("Personal Info", {'fields': ("first_name", "last_name")}),        
        ("Permissions", {'fields': ("is_staff", "is_creator", "is_active", "is_validated")}),
        ("Important dates", {'fields': ("last_login", "date_joined")}),
    )

    readonly_fields = ("last_login", "date_joined")


    add_fieldsets = (
        (None, {'fields': ("email", "username", "password1", "password2")}),
        ("Personal Info", {'fields': ("first_name", "last_name")}),    
        ("Permissions", {'fields': ("is_staff", "is_active")}),
    )


admin.site.register(GrowUser, GrowUserAdminConfig)