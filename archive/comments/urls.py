from django.conf.urls import url

from .views import CommentThreadView, CommentReplyView, CommentDeleteView

app_name = "comments"

# Commented out the url's leading to function based views
urlpatterns = [
    # url(r"^thread/(?P<content>\w+)/(?P<pk>\d+)", thread, name="thread"),
    url(r"^thread/(?P<content>\w+)/(?P<pk>\d+)/$", CommentThreadView.as_view(), name="thread"),
    # url(r"^reply/(?P<comment>\d+)", reply, name="reply"),
    url(r"^reply/(?P<comment>\d+)/$", CommentReplyView.as_view(), name="reply"),
    url(r"^delete/(?P<comment>\d+)/$", CommentDeleteView.as_view(), name="delete"),
]
