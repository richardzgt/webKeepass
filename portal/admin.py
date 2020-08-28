from django.contrib import admin
from portal.models import UserProfile
from django.contrib.auth.models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'password', 'email']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'secret_key', 'qrcode_img_file')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

