"""GeekText URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from books import views as book_view

from . import views, forms

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', book_view.list_books, name='home'),
    url(r"^accounts/", include("accounts.urls", namespace="accounts")),
    url(r"^accounts/avatar/", include('avatar.urls')),
    url(r"^book/", include("books.urls", namespace="books")),
    url(r"^password-reset/$", auth_views.PasswordResetView.as_view(form_class=forms.PasswordReset),
        name='forgot_password'),
    url(r"^password-reset/done/$", auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r"^password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        auth_views.PasswordResetConfirmView.as_view(form_class=forms.PasswordResetConfirm),
        name='password_reset_confirm'),
    url(r"^password-reset/complete/$", auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT})
    ]
