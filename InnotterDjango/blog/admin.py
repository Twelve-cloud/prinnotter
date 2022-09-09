from django.contrib import admin
from blog.models import Tag, Page, Post


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)


class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid', 'owner', 'is_private')
    list_display_links = ('name', 'uuid')
    search_fields = ('name', 'uuid', 'owner', 'is_private')


class PostAdmin(admin.ModelAdmin):
    list_display = ('page', 'content', 'created_at', 'updated_at')
    list_display_links = ('page', 'content')
    search_fields = ('page', 'content')


admin.site.register(Tag, TagAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Post, PostAdmin)
