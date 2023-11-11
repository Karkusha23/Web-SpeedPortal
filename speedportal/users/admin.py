from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserRegistrationForm, UserProfileForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = UserRegistrationForm
    form = UserProfileForm
    model = User
    prepopulated_fields = {'slug': ('username',)}
    list_display = ('username', 'email', 'is_staff', 'is_active',)
    list_filter = ('username', 'email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'slug', 'email', 'password')}),
        ('Дополнительное', {'fields': ('pfp', 'about', 'points')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'is_staff',
                'is_active', 'groups', 'user_permissions'
            )}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)



admin.site.register(User, CustomUserAdmin)