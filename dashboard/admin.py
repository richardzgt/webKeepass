from django.contrib import admin
from .models import Item, ItemGroup, CustomKV
from django.contrib.auth.models import User


class ItemAdmin(admin.ModelAdmin):
    pass

class ItemGroupAdmin(admin.ModelAdmin):
    pass

class CustomKVAdmin(admin.ModelAdmin):
    pass

admin.site.register(Item, ItemAdmin)
admin.site.register(ItemGroup, ItemGroupAdmin)
admin.site.register(CustomKV, CustomKVAdmin)
