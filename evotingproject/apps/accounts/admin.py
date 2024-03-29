from django.contrib import admin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
#REGISTERS ALL THE MODELS TO ADMIN SITE
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("password",)}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    add_form = CustomUserCreationForm # Here
    form = CustomUserChangeForm # Here
    change_password_form = AdminPasswordChangeForm # Here
    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

admin.site.register(CustomUser, CustomUserAdmin) # Here

from django.contrib import admin
from django.apps import apps

post_models = apps.get_app_config('accounts').get_models()

for model in post_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass