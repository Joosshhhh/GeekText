from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

from . import views

urlpatterns = [
    url(r'^$', views.cart_home)
]
