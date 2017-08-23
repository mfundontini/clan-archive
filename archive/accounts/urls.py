from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import LoginView, RegisterView, logout_view

app_name = "accounts"

urlpatterns = [
    url(r"^login/$", LoginView.as_view(), name="login"),
    url(r"^register/$", RegisterView.as_view(), name="register"),
    url(r"^logout/$", login_required(logout_view), name="logout"),
]
