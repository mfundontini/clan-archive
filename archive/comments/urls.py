from django.conf.urls import url

from .views import home, create, detail, update, delete

app_name = "posts"

urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^create/', create, name="create"),
    url(r"^detail/(?P<pk>\d+)", detail, name="detail"),
    url(r"^update/(?P<pk>\d+)", update, name="update"),
    url(r"^delete/(?P<pk>\d+)", delete, name="delete"),
]
