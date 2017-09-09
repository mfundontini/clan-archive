from django.conf.urls import url

from .views import (
    CommentListAPIView,
    ParentListAPIView,
    ChildrenListAPIView,
)

urlpatterns = [
    url(r'^$', CommentListAPIView.as_view(), name="list"),
    url(r'^parent/', ParentListAPIView.as_view(), name="parents"),
    url(r"^child/", ChildrenListAPIView.as_view(), name="children"),
]
