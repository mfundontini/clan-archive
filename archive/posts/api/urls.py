from django.conf.urls import url

from .views import PostListAPIView

urlpatterns = [
    url(r'^$', PostListAPIView.as_view(), name="list"),
    # url(r'^create/', create, name="create"),
    # url(r"^detail/(?P<pk>\d+)", detail, name="detail"),
    # url(r"^update/(?P<pk>\d+)", update, name="update"),
    # url(r"^delete/(?P<pk>\d+)", delete, name="delete"),
]
