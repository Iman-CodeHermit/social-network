from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User, OtpCode
from django.contrib.auth.models import Group

# Register your models here.

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'username')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'phone_number', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'bio', 'birthday')}),
        ('permissions', {'fields': ('is_active', 'is_admin')}),
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'last_name', 'first_name', 'birthday', 'password1', 'password2')}),
    )

    readonly_fields = ('last_login',)
    search_fields = ('username',)
    ordering = ('last_login',)
    filter_horizontal = ()

admin.site.unregister(Group)
admin.site.register(User, UserAdmin)


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')
