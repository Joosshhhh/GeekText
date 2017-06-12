from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.list_books, name="home"),
    url(r'^(?P<id>\d)/$', views.detail, name="search"),
    url(r'^author/(?P<id>\d)/$', views.author_books, name="book_author")


]
