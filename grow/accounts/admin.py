from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import GrowUser

class GrowUserAdminConfig(UserAdmin):
    search_fields = ("email", "user_name")
    list_display = ("email", "user_name", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff")
    ordering = ("user_name",)
    
    fieldsets = (
        (None, {'fields': ("email", "user_name")}),
        ("Personal Info", {'fields': ("first_name", "last_name")}),        
        ("Permissions", {'fields': ("is_staff", "is_active")}),
        ("Important dates", {'fields': ("last_login", "date_joined")}),
    )

    readonly_fields = ("last_login", "date_joined")


    add_fieldsets = (
        (None, {'fields': ("email", "user_name", "password1", "password2")}),
        ("Personal Info", {'fields': ("first_name", "last_name")}),    
        ("Permissions", {'fields': ("is_staff", "is_active")}),
    )


admin.site.register(GrowUser, GrowUserAdminConfig)