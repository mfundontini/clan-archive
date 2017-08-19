from django.conf.urls import url

from .views import thread, reply, CommentThreadView

app_name = "comments"

urlpatterns = [
    url(r"^thread/(?P<content>\w+)/(?P<pk>\d+)", thread, name="thread"),
    url(r"^cbv/(?P<content>\w+)/(?P<pk>\d+)/$", CommentThreadView.as_view(), name="cbv_thread"),
    url(r"^reply/(?P<comment>\d+)", reply, name="reply"),
]
