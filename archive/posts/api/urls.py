from django.conf.urls import url

from .views import (
    PostListAPIView,
    PostDetailAPIView,
    PostUpdateAPIView,
    PostDeleteAPIView,
    PostCreateAPIView
)

urlpatterns = [
    url(r'^$', PostListAPIView.as_view(), name="list"),
    url(r'^create/', PostCreateAPIView.as_view(), name="create"),
    url(r"^detail/(?P<slug>(\w+-?)+)$", PostDetailAPIView.as_view(), name="detail"),
    url(r"^update/(?P<pk>\d+)$", PostUpdateAPIView.as_view(), name="update"),
    url(r"^delete/(?P<pk>\d+)$", PostDeleteAPIView.as_view(), name="delete"),
]
