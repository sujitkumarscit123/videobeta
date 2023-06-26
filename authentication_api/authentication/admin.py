from django.contrib import admin
from .models import User, Role, UserRole, Courses, CourseUsers


class UserRoleInline(admin.TabularInline):
    model = UserRole


class UserAdmin(admin.ModelAdmin):
    inlines = [UserRoleInline]


admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(Courses)
admin.site.register(CourseUsers)
