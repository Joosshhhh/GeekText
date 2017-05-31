from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views, forms

urlpatterns = [
    url(r"^register/$", views.RegisterView.as_view(), name='register'),
    url(r"^login/$", auth_views.LoginView.as_view(authentication_form=forms.Login), name='login'),
    url(r"^logout/$", views.LogoutView.as_view(), name='logout'),
    url(r"^reactivate/$", views.ReactivateAccountView.as_view(), name='reactivate'),
    url(r"^deactivate/$", views.DeactivateAccountView.as_view(), name='deactivate'),
    url(r"^deactivated/$", views.DeactivatedAccountView.as_view(), name='deactivated'),
    url(r"^manage/$", views.ManageAccountView.as_view(), name='manage'),
    url(r"^manage/profile/$", views.ManageProfileView.as_view(), name='manage_profile'),
    url(r"^manage/profile/firstname/$", views.AccountUpdateFirstNameView.as_view(), name='manage_profile_first_name'),
    url(r"^manage/profile/lastname/$", views.AccountUpdateLastNameView.as_view(), name='manage_profile_last_name'),
    url(r"^manage/profile/email/$", views.AccountUpdateEmailView.as_view(), name='manage_profile_email'),
    url(r"^manage/profile/username/$", views.AccountUpdateUsernameView.as_view(), name='manage_profile_username'),
    url(r"^manage/profile/password/$", views.AccountUpdatePasswordView.as_view(), name='manage_profile_password'),
    url(r"^manage/addresses$", views.ManageAddressView.as_view(), name='manage_addresses'),
    url(r"^manage/new-address$", views.AddressAddView.as_view(), name='manage_new_address'),
    url(r"^manage/address/(?P<pk>\d+)/$", views.AddressUpdateView.as_view(), name='manage_address'),
    url(r"^manage/delete-address/(?P<pk>\d+)/$", views.AddressDeleteView.as_view(), name='manage_delete_address'),
    url(r"^manage/payment/$", views.ManagePaymentView.as_view(), name='manage_payment'),
    url(r"^manage/new-payment$", views.PaymentAddView.as_view(), name='manage_new_payment'),
    url(r"^manage/delete-payment/(?P<pk>\d+)/$", views.PaymentDeleteView.as_view(), name='manage_delete_payment'),

]
