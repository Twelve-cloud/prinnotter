from django.contrib import admin
from user.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'role', 'is_blocked')
    list_display_links = ('email', 'username')
    search_fields = ('email', 'username')


admin.site.register(User, UserAdmin)
