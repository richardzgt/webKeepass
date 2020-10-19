from django.contrib import admin
from portal.models import UserProfile, SysLog
from django.contrib.auth.models import User
# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext, gettext_lazy as _
from django import forms
#
# Override username field require email address
class UserCreationForm2(UserCreationForm):
    email = forms.CharField(max_length=75, required=True)
class UserChangeForm2(UserChangeForm):
    email = forms.CharField(max_length=75, required=True)

class UserAdmin2(UserAdmin):
    form = UserChangeForm2
    # add_form = UserCreationForm2
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', )}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        })
    )

admin.site.unregister(User)
admin.site.register(User, UserAdmin2)


class UserAdmin(admin.ModelAdmin):
    # fields = ['username', 'password', 'email']
    # fields = ['username', 'password', 'email']
    list_display = ['user', 'secret_key', 'qrcode_img_file']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'secret_key', 'qrcode_img_file')

class SysLogAdmin(admin.ModelAdmin):
    # list_display = '__all__'
    list_display = ('user', 'ip', 'action', 'attr', 'message', 'created_at')

# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserAdmin)
admin.site.register(SysLog, SysLogAdmin)

