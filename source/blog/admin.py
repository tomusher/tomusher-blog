from django.contrib import admin
from .models import Post, Image

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class ImageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Post, PostAdmin)
admin.site.register(Image, ImageAdmin)
