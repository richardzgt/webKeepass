from django.contrib import admin
from portal.models import UserProfile, SysLog
from django.contrib.auth.models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'password', 'email']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'secret_key', 'qrcode_img_file')

class SysLogAdmin(admin.ModelAdmin):
    # list_display = '__all__'
    list_display = ('user', 'ip', 'action', 'attr', 'message', 'created_at')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(SysLog, SysLogAdmin)

