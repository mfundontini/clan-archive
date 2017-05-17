from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Post, User


# Register your models here.
class PostAdminInline(admin.StackedInline):
    model = Post
    can_delete = False
    verbose_name = "Post"
    verbose_name_plural = "Authored Posts"
    fields = ["title"]


class UserAdmin(BaseUserAdmin):
    inlines = (PostAdminInline, )


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

