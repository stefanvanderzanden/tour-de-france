from django.contrib import admin

from apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = [
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_superuser",
        # "groups",
        # "user_permissions"
    ]
    list_display = ["last_name", "first_name", "email"]
