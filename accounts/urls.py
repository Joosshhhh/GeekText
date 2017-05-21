from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views, forms

urlpatterns = [
    url(r"^login/$", auth_views.LoginView.as_view(authentication_form=forms.Login), name='login'),
    url(r"^logout/$", views.LogoutView.as_view(), name='logout'),
    url(r"^manage/$", views.ManageAccountView.as_view(), name='manage'),
    url(r"^manage/payment$", views.ManagePaymentView.as_view(), name='manage_payment'),
    url(r"^manage/settings$", views.ManageAccountSettingsView.as_view(), name='manage_settings'),
    url(r"^manage/address$", views.ManageAddressView.as_view(), name='manage_address'),
    url(r"^register/$", views.RegisterView.as_view(), name='register'),
]
