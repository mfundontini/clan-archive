from django.conf.urls import url

from .views import (
    CommentListAPIView,
    ParentListAPIView,
    ChildrenListAPIView,
    CommentDetailAPIView,
)

urlpatterns = [
    url(r'^$', CommentListAPIView.as_view(), name="list"),
    url(r'^parent/', ParentListAPIView.as_view(), name="parents"),
    url(r"^child/", ChildrenListAPIView.as_view(), name="children"),
    url(r"^(?P<pk>\d+)/$", CommentDetailAPIView.as_view(), name="detail"),
]
