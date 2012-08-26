from blog.models import Post
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
    list_display        = ('title', 'publish', 'status')
    list_filter         = ('publish', 'status')
    search_fields       = ('title', 'body', 'tease')

admin.site.register(Post, PostAdmin)
