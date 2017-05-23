from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views, forms

urlpatterns = [
    url(r"^login/$", auth_views.LoginView.as_view(authentication_form=forms.Login), name='login'),
    url(r"^logout/$", views.LogoutView.as_view(), name='logout'),
    url(r"^manage/$", views.ManageAccountView.as_view(), name='manage'),
    url(r"^manage/payment/$", views.ManagePaymentView.as_view(), name='manage_payment'),
    url(r"^manage/profile/$", views.ManageProfileView.as_view(), name='manage_profile'),
    url(r"^manage/profile/firstname/$", views.AccountUpdateFirstNameView.as_view(), name='manage_profile_first_name'),
    url(r"^manage/profile/lastname/$", views.AccountUpdateLastNameView.as_view(), name='manage_profile_last_name'),
    url(r"^manage/profile/email/$", views.AccountUpdateEmailView.as_view(), name='manage_profile_email'),
    url(r"^manage/profile/username/$", views.AccountUpdateUsernameView.as_view(), name='manage_profile_username'),
    url(r"^manage/profile/password/$", views.AccountUpdatePasswordView.as_view(), name='manage_profile_password'),
    url(r"^manage/address$", views.ManageAddressView.as_view(), name='manage_address'),
    url(r"^register/$", views.RegisterView.as_view(), name='register'),
]
