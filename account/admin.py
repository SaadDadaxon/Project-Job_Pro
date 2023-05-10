from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import AccountFormsCreate, AccountChangeForms

from .models import Account


@admin.action(description="Set to HR")
def set_to_hr(modeladmin, request, queryset):
    queryset.update(role=0, is_staff=False)


@admin.action(description="Set to Candidate")
def set_to_candidate(modeladmin, request, queryset):
    queryset.update(role=0, is_staff=False)


@admin.action(description="Set to Admin")
def set_to_admin(modeladmin, request, queryset):
    queryset.update(role=0, is_staff=True)


class AccountAdmin(UserAdmin):
    form = AccountChangeForms
    add_form = AccountFormsCreate
    add_fieldsets = (
        (None, {"classes": ('wide', ), "fields": ('email', 'role', "password", "password2"), }),
    )
    list_display = ('id', 'email', 'full_name', 'image_tag', 'get_role_display', 'bio', 'is_superuser', 'is_active',
                    'is_staff', 'modified_date', 'created_date')
    readonly_fields = ('created_date', 'modified_date')
    actions = [set_to_candidate, set_to_hr]
    list_filter = ('modified_date', 'role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {"fields": ('email', 'password', 'full_name', 'image'), }),
        ("Permission", {'fields': ('role', 'is_superuser', 'is_active', 'is_staff', 'groups', 'user_permissions'), }),
        ("Important dates", {'fields': ('modified_date', 'created_date'), }),
    )
    ordering = None
    search_fields = ('email', 'full_name')


admin.site.register(Account, AccountAdmin)


