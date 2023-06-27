from django.contrib import admin
from .models import User, Role, UserRole


class UserRoleInline(admin.TabularInline):
    model = UserRole


class UserAdmin(admin.ModelAdmin):
    inlines = [UserRoleInline]


admin.site.register(User, UserAdmin)
admin.site.register(Role)
