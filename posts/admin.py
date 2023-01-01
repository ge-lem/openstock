from django.contrib import admin
from posts.models import Post, PhotoPost

@admin.register(PhotoPost)
class PhotoPostAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
