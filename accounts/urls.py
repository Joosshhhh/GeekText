from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.static import serve

from . import views, forms

urlpatterns = [
    url(r"^login/$", auth_views.LoginView.as_view(authentication_form=forms.Login), name='login'),
    url(r"^logout/$", views.LogoutView.as_view(), name='logout'),
    url(r"^deactivate/$", views.DeactivateAccountView, name='deactivate'),
    url(r"^manage/$", views.ManageAccountView.as_view(), name='manage'),
    url(r"^manage/profile/$", views.ManageProfileView.as_view(), name='manage_profile'),
    url(r"^manage/profile/avatar/$", views.AccountUpdateAvatarView.as_view(), name='manage_profile_avatar'),
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
    url(r"^register/$", views.RegisterView.as_view(), name='register'),

]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT})
    ]
