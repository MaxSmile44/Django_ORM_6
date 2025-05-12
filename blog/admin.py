from django.contrib import admin
from blog.models import Post, Tag, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    raw_id_fields = ('likes',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author')
    raw_id_fields = ('author',)


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
