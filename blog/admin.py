from django.contrib import admin
from blog.models import Category
from blog.models import Post
from blog.models import Comment
from blog.models import Tag


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = ('name', )

admin.site.register(Category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'created_at', )
    search_fields = ('title', 'content', )

admin.site.register(Post, PostAdmin)

admin.site.register(Comment)
admin.site.register(Tag)
