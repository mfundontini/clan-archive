from django.contrib import admin

from .models import Post


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "author", "created"]
    list_display_links = ["__unicode__"]
    list_editable = ["author"]
    search_fields = ["title", "body"]
    list_filter = ["created"]

    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)

