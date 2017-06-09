from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.list_books),
    url(r'^(?P<id>\d)/$', views.detail, name="search"),


]
