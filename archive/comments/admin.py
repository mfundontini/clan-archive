from django.contrib import admin

from archive.comments.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "date_added"]
    list_display_links = ["__unicode__"]
    search_fields = ["__unicode__", "body"]
    list_filter = ["date_added"]

admin.site.register(Comment, CommentAdmin)
