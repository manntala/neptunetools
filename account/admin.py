from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import Account, Profile

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active',)
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image',)
    search_fields = ('user',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Profile, ProfileAdmin)
