from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.BookListView.as_view(), name="book_list"),
    url(r'^(?P<pk>\d+)/$', views.BookDetailView.as_view(), name="book_detail"),
    url(r'^(?P<pk>\d+)/review/$', views.write_review, name="book_write"),
    url(r'^authors/$', views.AllAuthorsView.as_view(), name="books_authors"),
    url(r'^author/(?P<pk>\d+)/$', views.author_books, name="books_author"),
    url(r'^remove_comment/(?P<pk>\d+)/$', views.remove_comment),
    url(r'^approve_comment/(?P<pk>\d+)/$', views.approve_comment),

]
