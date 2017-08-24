"""blog19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include, static
from django.contrib import admin
from django.conf import settings

import object_tools

from archive.posts.views import home

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^object-tools/', include(object_tools.tools.urls)),
    # url(r'^formfactory/', include("formfactory.urls", namespace="formfactory")),
    url(r"^post/", include("archive.posts.urls", namespace="posts")),
    url(r"^comment/", include("archive.comments.urls", namespace="comments")),
    url(r"^account/", include("archive.accounts.urls", namespace="accounts")),
    url(r"^api/post/", include("archive.posts.api.urls", namespace="posts-api")),
    url(r"^$", home),
]

if settings.DEBUG:
    urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
