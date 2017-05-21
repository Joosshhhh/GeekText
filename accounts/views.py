from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views import generic

from . import forms


class ManageAccountView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/manage.html'


class ManagePaymentView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/manage_payment.html'


class ManageAddressView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/manage_address.html'


class AccountSettingsUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.AccountUpdateProfile
    success_url = reverse_lazy("accounts:manage")
    template_name = 'accounts/manage_account.html'

    def get_object(self, queryset=None):
        return self.request.user


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
