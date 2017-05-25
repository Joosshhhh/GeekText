from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.urlresolvers import reverse_lazy
from django.views import generic

from . import forms
from .models import UserAddress


class DeactivateAccountView(LoginRequiredMixin, generic.FormView):
    form_class = forms.DeactivateForm
    success_url = reverse_lazy("home")

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())


class AddAddressView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.UserAddressForm
    success_url = reverse_lazy("accounts:manage_addresses")
    template_name = "accounts/manage_address_form.html"

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(AddAddressView, self).form_valid(form)


class AddressUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.UserAddressForm
    success_url = reverse_lazy("accounts:manage_addresses")
    template_name = 'accounts/manage_address_form.html'

    def get_object(self, queryset=None):
        return UserAddress.objects.get(pk=self.kwargs['pk'])


class ManageAccountView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/manage.html'


class ManagePaymentView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/manage_payment.html'


class ManageAddressView(LoginRequiredMixin, generic.ListView):
    template_name = 'accounts/manage_address.html'

    def get_queryset(self):
        """Returns Polls that belong to the current user"""
        return UserAddress.objects.filter(user=self.request.user).all()


class ManageProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/manage_profile.html'


class AccountUpdateFirstNameView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.AccountUpdateFirstName
    success_url = reverse_lazy("accounts:manage_profile")
    template_name = 'accounts/profile/manage_first_name.html'

    def get_object(self, queryset=None):
        return self.request.user


class AccountUpdateLastNameView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.AccountUpdateLastName
    success_url = reverse_lazy("accounts:manage_profile")
    template_name = 'accounts/profile/manage_last_name.html'

    def get_object(self, queryset=None):
        return self.request.user


class AccountUpdateEmailView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.AccountUpdateEmail
    success_url = reverse_lazy("accounts:manage_profile")
    template_name = 'accounts/profile/manage_email.html'

    def get_object(self, queryset=None):
        return self.request.user


class AccountUpdateUsernameView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.AccountUpdateUsername
    success_url = reverse_lazy("accounts:manage_profile")
    template_name = 'accounts/profile/manage_username.html'

    def get_object(self, queryset=None):
        return self.request.user


class AccountUpdatePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = forms.AccountUpdatePassword
    success_url = reverse_lazy("accounts:manage_profile")
    template_name = 'accounts/profile/manage_password.html'


class LoginView(generic.FormView):
    form_class = forms.Login
    success_url = reverse_lazy("home")

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogoutView(generic.RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class RegisterView(generic.CreateView):
    form_class = forms.Register
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/register.html"
