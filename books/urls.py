from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.list_books, name="home"),
    url(r'^(?P<id>\d)/$', views.detail, name="search"),
    url(r'^(?P<id>\d)/review/$', views.write_review, name="book_write"),
    url(r'^author/(?P<id>\d)/$', views.author_books, name="book_author"),
    url(r'^remove_comment/(?P<pk>\d+)/$', views.remove_comment),
    url(r'^approve_comment/(?P<pk>\d+)/$', views.approve_comment),

]
