from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Post, User


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
admin.site.register(User, UserAdmin)

