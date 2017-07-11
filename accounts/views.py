import pyxb
import re

from authorizenet.apicontrollers import *
from django import forms
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from cart.views import cart_count

from . import forms, models

CARDS = {
    'Amex': re.compile(r"^3[47][0-9]{13}$"),
    'Diners Club': re.compile(r"^3(?:0[0-5]|[68][0-9])[0-9]{11}$"),
    'Discover': re.compile(
        r"^65[4-9][0-9]{13}|64[4-9][0-9]{13}|6011[0-9]{12}|(622(?:12[6-9]|1[3-9][0-9]|[2-8][0-9][0-9]|9[01][0-9]|92[0-5])[0-9]{10})$"),
    'JCB': re.compile(r"^(?:2131|1800|35\d{3})\d{11}$"),
    'Maestro ': re.compile(r"^(5018|5020|5038|6304|6759|6761|6763)[0-9]{8,15}$"),
    'Mastercard': re.compile(r"^5[1-5][0-9]{14}$"),
    "Solo": re.compile(r"^(6334|6767)[0-9]{12}|(6334|6767)[0-9]{14}|(6334|6767)[0-9]{15}$"),
    'Switch': re.compile(
        r"^(4903|4905|4911|4936|6333|6759)[0-9]{12}|(4903|4905|4911|4936|6333|6759)[0-9]{14}|(4903|4905|4911|4936|6333|6759)[0-9]{15}|564182[0-9]{10}|564182[0-9]{12}|564182[0-9]{13}|633110[0-9]{10}|633110[0-9]{12}|633110[0-9]{13}$"),
    'Union Pay': re.compile(r"^(62[0-9]{14,17})$"),
    'Visa': re.compile(r"^4[0-9]{12}(?:[0-9]{3})?$"),
    'Visa Mastercard': re.compile(r"^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})$"),
}


def get_vendor(number):
    """Return the type if it matches one of the cards."""
    for card, pattern in CARDS.items():
        if pattern.match(number):
            return card
    return None


class RegisterView(generic.CreateView):
    form_class = forms.Register
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/register.html"

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        number = cart_count(self.request)
        context['number'] = number
        return context


class LoginView(generic.FormView):
    form_class = forms.Login
    success_url = reverse_lazy("home")
    template_name = "registration/login.html"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        number = cart_count(self.request)
        context['number'] = number
        return context


class LogoutView(generic.RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class DeactivateAccountView(LoginRequiredMixin, generic.RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        self.request.user.is_active = False
        self.request.user.save()
        logout(request)
        return super().get(request, *args, **kwargs)


class ReactivateAccountView(LoginRequiredMixin, generic.RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        self.request.user.is_active = True
        self.request.user.save()
        return super().get(request, *args, **kwargs)


class DeactivatedAccountView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/deactivated.html'

    def get_context_data(self, **kwargs):
        context = super(DeactivatedAccountView, self).get_context_data(**kwargs)
        number = cart_count(self.request)
        context['number'] = number

        return context


class ManageAccountView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/manage.html'

    def get_context_data(self, **kwargs):
        context = super(ManageAccountView, self).get_context_data(**kwargs)
        number = cart_count(self.request)
        context['number'] = number

        return context


class AccountUpdateFirstNameView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.AccountUpdateFirstName
    success_url = reverse_lazy("accounts:manage_profile")
    template_name = 'accounts/profile/manage_first_name.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(AccountUpdateFirstNameView, self).get_context_data(**kwargs)
        number = cart_count(self.request)
        context['number'] = number
        return context


class AccountUpdateLastNameView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.AccountUpdateLastName
    success_url = reverse_lazy("accounts:manage_profile")
    template_name = 'accounts/profile/manage_last_name.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(AccountUpdateLastNameView, self).get_context_data(**kwargs)
        number = cart_count(self.request)
        context['number'] = number
        return context


class AccountUpdateEmailView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.AccountUpdateEmail
    success_url = reverse_lazy("accounts:manage_profile")
    template_name = 'accounts/profile/manage_email.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(AccountUpdateEmailView, self).get_context_data(**kwargs)
        number = cart_count(self.request)
        context['number'] = number
        return context


class AccountUpdateUsernameView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.AccountUpdateUsername
    success_url = reverse_lazy("accounts:manage_profile")
    template_name = 'accounts/profile/manage_username.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(AccountUpdateUsernameView, self).get_context_data(**kwargs)
        number = cart_count(self.request)
        context['number'] = number
        return context


class AccountUpdatePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = forms.AccountUpdatePassword
    success_url = reverse_lazy("accounts:manage_profile")
    template_name = 'accounts/profile/manage_password.html'

    def get_context_data(self, **kwargs):
        context = super(AccountUpdatePasswordView, self).get_context_data(**kwargs)
        number = cart_count(self.request)
        context['number'] = number
        return context


class ManageProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/manage_profile.html'

    def get_context_data(self, **kwargs):
        context = super(ManageProfileView, self).get_context_data(**kwargs)
        number = cart_count(self.request)
        context['number'] = number

        return context


class AddressAddView(LoginRequiredMixin, generic.FormView):
    form_class = forms.UserAddressForm
    success_url = reverse_lazy("accounts:manage_addresses")
    template_name = "accounts/manage_address_form.html"

    def form_valid(self, form):
        form.add_shipping_address(self.request.user.authorize_net_profile_id)
        return super(AddressAddView, self).form_valid(form)

    def get_initial(self):
        initial = super(AddressAddView, self).get_initial()
        initial['country'] = "US"
        return initial

    def get_context_data(self, **kwargs):
        context = super(AddressAddView, self).get_context_data(**kwargs)
        number = cart_count(self.request)
        context['number'] = number

        return context


class AddressUpdateView(LoginRequiredMixin, generic.FormView):
    form_class = forms.UserAddressForm
    success_url = reverse_lazy("accounts:manage_addresses")
    template_name = 'accounts/manage_address_form.html'

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(AddressUpdateView, self).get_initial()

        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = settings.AUTHORIZENET_LOGIN_ID
        merchantAuth.transactionKey = settings.AUTHORIZENET_TRANS_KEY

        # create get shipping address request
        getShippingAddress = apicontractsv1.getCustomerShippingAddressRequest()
        getShippingAddress.merchantAuthentication = merchantAuth
        getShippingAddress.customerProfileId = self.request.user.authorize_net_profile_id
        getShippingAddress.customerAddressId = self.kwargs.get('pk')

        # Make the API call
        getShippingAddressController = getCustomerShippingAddressController(getShippingAddress)
        getShippingAddressController.execute()
        response = getShippingAddressController.getresponse()

        if response.messages.resultCode == "Ok":

            initial['country'] = response.address.country
            initial['first_name'] = response.address.firstName
            initial['last_name'] = response.address.lastName
            initial['address'] = response.address.address

            initial['city'] = response.address.city
            initial['state'] = response.address.state
            initial['zipcode'] = response.address.zip
            initial['phone'] = response.address.phoneNumber
            if hasattr(response, 'defaultShippingAddress'):
                if response.defaultShippingAddress:
                    initial['default'] = response.defaultShippingAddress

        else:
            print("ERROR")
            print("Message text : %s " % response.messages.message[0]['text'].text)

        return initial

    def form_valid(self, form):
        form.update_shipping_address(self.request.user.authorize_net_profile_id, self.kwargs.get('pk'))
        return super(AddressUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddressUpdateView, self).get_context_data(**kwargs)
        number = cart_count(self.request)
        context['number'] = number

        return context


class AddressDeleteView(LoginRequiredMixin, generic.RedirectView):
    url = reverse_lazy('accounts:manage_addresses')

    def get(self, request, *args, **kwargs):

        # Give merchant details
        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = settings.AUTHORIZENET_LOGIN_ID
        merchantAuth.transactionKey = settings.AUTHORIZENET_TRANS_KEY

        # create delete request
        deleteShippingAddress = apicontractsv1.deleteCustomerShippingAddressRequest()
        deleteShippingAddress.merchantAuthentication = merchantAuth
        deleteShippingAddress.customerProfileId = self.request.user.authorize_net_profile_id
        deleteShippingAddress.customerAddressId = self.kwargs.get('pk')

        # Make the API call
        deleteShippingAddressController = deleteCustomerShippingAddressController(deleteShippingAddress)
        deleteShippingAddressController.execute()
        response = deleteShippingAddressController.getresponse()

        if response.messages.resultCode == "Ok":
            print("SUCCESS")
            print("Message text : %s " % response.messages.message[0]['text'].text)
        else:
            print("ERROR")
            print("Message text : %s " % response.messages.message[0]['text'].text)

        return super().get(request, *args, **kwargs)


class ManageAddressView(LoginRequiredMixin, generic.ListView):
    template_name = 'accounts/manage_address.html'
    default_list = [0]

    def get_queryset(self):
        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = settings.AUTHORIZENET_LOGIN_ID
        merchantAuth.transactionKey = settings.AUTHORIZENET_TRANS_KEY

        getCustomerProfile = apicontractsv1.getCustomerProfileRequest()
        getCustomerProfile.merchantAuthentication = merchantAuth
        getCustomerProfile.customerProfileId = self.request.user.authorize_net_profile_id
        controller = getCustomerProfileController(getCustomerProfile)
        controller.execute()

        response = controller.getresponse()

        if response.messages.resultCode == "Ok":
            if hasattr(response.profile, 'shipToList'):
                for address in response.profile.shipToList:

                    getShippingAddress = apicontractsv1.getCustomerShippingAddressRequest()
                    getShippingAddress.merchantAuthentication = merchantAuth
                    getShippingAddress.customerProfileId = self.request.user.authorize_net_profile_id
                    getShippingAddress.customerAddressId = str(address.customerAddressId)

                    # Make the API call
                    getShippingAddressController = getCustomerShippingAddressController(getShippingAddress)
                    getShippingAddressController.execute()
                    response2 = getShippingAddressController.getresponse()

                    if response2.messages.resultCode == "Ok":
                        if hasattr(response2, 'defaultShippingAddress'):
                            if response2.defaultShippingAddress:
                                print(len(self.default_list))
                                self.default_list.append(address.customerAddressId)
                                print(len(self.default_list))
                        else:
                            if address.customerAddressId in self.default_list:
                                self.default_list.remove(address.customerAddressId)
                    else:
                        print("ERROR")
                        print("Message text : %s " % response.messages.message[0]['text'].text)

                else:
                    print("No addresses yet")

                return response.profile.shipToList

        return None

    def get_context_data(self, **kwargs):
        context = super(ManageAddressView, self).get_context_data(**kwargs)
        number = cart_count(self.request)
        context['number'] = number
        context['default'] = self.default_list
        return context


class PaymentAddView(LoginRequiredMixin, generic.FormView):
    form_class = forms.UserPaymentForm
    success_url = reverse_lazy("accounts:manage_payment")
    template_name = "accounts/manage_payment_form.html"

    def form_valid(self, form):
        p = models.UserPayments.objects.create(user=self.request.user)
        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = settings.AUTHORIZENET_LOGIN_ID
        merchantAuth.transactionKey = settings.AUTHORIZENET_TRANS_KEY
        try:
            card_number = form.cleaned_data.get('card_first') + form.cleaned_data.get(
                'card_second') + form.cleaned_data.get(
                'card_third') + form.cleaned_data.get('card_fourth')

            creditCard = apicontractsv1.creditCardType()
            creditCard.cardNumber = card_number
            creditCard.expirationDate = form.cleaned_data.get('exp_year') + "-" + form.cleaned_data.get('exp_month')
            creditCard.cardCode = form.cleaned_data.get('ccv')

            payment = apicontractsv1.paymentType()
            payment.creditCard = creditCard

            billTo = apicontractsv1.customerAddressType()
            billTo.firstName = self.request.user.first_name
            billTo.lastName = self.request.user.last_name
        except pyxb.SimpleFacetValueError:
            form.add_error(None, 'Invalid input.')
            return super(PaymentAddView, self).form_invalid(form)
        getCustomerProfile = apicontractsv1.getCustomerProfileRequest()
        getCustomerProfile.merchantAuthentication = merchantAuth
        getCustomerProfile.customerProfileId = self.request.user.authorize_net_profile_id
        controller = getCustomerProfileController(getCustomerProfile)
        controller.execute()

        response = controller.getresponse()

        if response.messages.resultCode == "Ok":
            if hasattr(response.profile, 'shipToList'):
                for address in response.profile.shipToList:

                    # create get shipping address request
                    getShippingAddress = apicontractsv1.getCustomerShippingAddressRequest()
                    getShippingAddress.merchantAuthentication = merchantAuth
                    getShippingAddress.customerProfileId = self.request.user.authorize_net_profile_id
                    getShippingAddress.customerAddressId = str(address.customerAddressId)

                    # Make the API call
                    getShippingAddressController = getCustomerShippingAddressController(getShippingAddress)
                    getShippingAddressController.execute()
                    response2 = getShippingAddressController.getresponse()

                    if response2.messages.resultCode == "Ok":
                        print("SUCCESS")
                        if hasattr(response2, 'defaultShippingAddress'):
                            if response2.defaultShippingAddress:
                                billTo.firstName = response2.address.firstName
                                billTo.lastName = response2.address.lastName
                                billTo.address = response2.address.address
                                billTo.city = response2.address.city
                                billTo.state = response2.address.state
                                billTo.zip = response2.address.zip
                                billTo.country = response2.address.country
                                billTo.phoneNumber = str(response2.address.phoneNumber)
                    else:
                        form.add_error(None, response2.messages.message[0]['text'].text)
                        return super(PaymentAddView, self).form_invalid(form)
            else:
                print('No shipping addresses')
        else:
            form.add_error(None, response.messages.message[0]['text'].text)
            return super(PaymentAddView, self).form_invalid(form)

        profile = apicontractsv1.customerPaymentProfileType()
        profile.payment = payment
        profile.billTo = billTo
        profile.customerType = 'individual'
        profile.defaultPaymentProfile = form.cleaned_data.get('default')

        createCustomerPaymentProfile = apicontractsv1.createCustomerPaymentProfileRequest()
        createCustomerPaymentProfile.merchantAuthentication = merchantAuth
        createCustomerPaymentProfile.paymentProfile = profile
        createCustomerPaymentProfile.customerProfileId = self.request.user.authorize_net_profile_id
        createCustomerPaymentProfile.validationMode = 'testMode'

        controller = createCustomerPaymentProfileController(createCustomerPaymentProfile)
        controller.execute()

        response3 = controller.getresponse()

        if response3.messages.resultCode == "Ok":
            print("Successfully created a customer payment profile with id: %s" % response3.customerPaymentProfileId)

            vendor = get_vendor(card_number)
            if vendor:
                p.card_company = vendor
                print(vendor)

            p.authorize_net_payment_profile_id = response3.customerPaymentProfileId
            p.full_name = form.cleaned_data.get('full_name')
            p.save()
        else:
            form.add_error(None, response3.messages.message[0]['text'].text)
            return super(PaymentAddView, self).form_invalid(form)

        return super(PaymentAddView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PaymentAddView, self).get_context_data(**kwargs)
        number = cart_count(self.request)
        context['number'] = number

        return context


class PaymentUpdateView(LoginRequiredMixin, generic.FormView):
    form_class = forms.UserPaymentForm
    success_url = reverse_lazy("accounts:manage_payment")
    template_name = 'accounts/manage_payment_form.html'

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(PaymentUpdateView, self).get_initial()

        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = settings.AUTHORIZENET_LOGIN_ID
        merchantAuth.transactionKey = settings.AUTHORIZENET_TRANS_KEY

        getCustomerPaymentProfile = apicontractsv1.getCustomerPaymentProfileRequest()
        getCustomerPaymentProfile.merchantAuthentication = merchantAuth
        getCustomerPaymentProfile.customerProfileId = self.request.user.authorize_net_profile_id
        getCustomerPaymentProfile.customerPaymentProfileId = self.kwargs.get('pk')
        getCustomerPaymentProfile.unmaskExpirationDate = True
        controller = getCustomerPaymentProfileController(getCustomerPaymentProfile)
        controller.execute()

        response = controller.getresponse()

        if response.messages.resultCode == "Ok":
            print("Successfully retrieved a payment profile with profile id %s and customer id %s" % (
                getCustomerPaymentProfile.customerProfileId, getCustomerPaymentProfile.customerProfileId))
            if hasattr(response, 'paymentProfile'):
                if hasattr(response.paymentProfile, 'payment'):
                    payment = models.UserPayments.objects.filter(
                        authorize_net_payment_profile_id=self.kwargs.get('pk')).first()
                    initial['full_name'] = payment.full_name
                    initial['card_first'] = 'XXXX'
                    initial['card_second'] = 'XXXX'
                    initial['card_third'] = 'XXXX'
                    initial['card_fourth'] = \
                        str(response.paymentProfile.payment.creditCard.cardNumber).split("XXXX", 1)[1]
                    initial['exp_month'] = str(response.paymentProfile.payment.creditCard.expirationDate).split("-", 1)[
                        1]
                    initial['exp_year'] = str(response.paymentProfile.payment.creditCard.expirationDate).split("-", 1)[
                        0]

                if hasattr(response.paymentProfile, 'defaultPaymentProfile'):
                    if response.paymentProfile.defaultPaymentProfile:
                        initial['default'] = response.paymentProfile.defaultPaymentProfile


        else:
            print("response code: %s" % response.messages.resultCode)
            print(
                "Failed to get payment profile information with id %s" % getCustomerPaymentProfile.customerPaymentProfileId)

        return initial

    def form_valid(self, form):
        card_number = form.cleaned_data.get('card_first') + form.cleaned_data.get(
            'card_second') + form.cleaned_data.get(
            'card_third') + form.cleaned_data.get('card_fourth')
        valid_input = card_number + form.cleaned_data.get('ccv') + form.cleaned_data.get(
            'exp_month') + form.cleaned_data.get('exp_year')
        if not valid_input.isdigit():
            form.add_error(None, 'Invalid input. Remember to replace XXXX with your valid card numbers')
            return super(PaymentUpdateView, self).form_invalid(form)
        form.update_payment(self.request.user.authorize_net_profile_id, self.kwargs.get('pk'), card_number)
        if form.cleaned_data.get('full_name'):
            payment = models.UserPayments.objects.filter(
                authorize_net_payment_profile_id=self.kwargs.get('pk')).first()
            payment.full_name = form.cleaned_data.get('full_name')
            payment.save()
        return super(PaymentUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PaymentUpdateView, self).get_context_data(**kwargs)
        number = cart_count(self.request)
        context['number'] = number

        return context


class PaymentDeleteView(LoginRequiredMixin, generic.RedirectView):
    url = reverse_lazy('accounts:manage_payment')

    def get(self, request, *args, **kwargs):

        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = settings.AUTHORIZENET_LOGIN_ID
        merchantAuth.transactionKey = settings.AUTHORIZENET_TRANS_KEY

        deleteCustomerPaymentProfile = apicontractsv1.deleteCustomerPaymentProfileRequest()
        deleteCustomerPaymentProfile.merchantAuthentication = merchantAuth
        deleteCustomerPaymentProfile.customerProfileId = self.request.user.authorize_net_profile_id
        deleteCustomerPaymentProfile.customerPaymentProfileId = self.kwargs.get('pk')

        controller = deleteCustomerPaymentProfileController(deleteCustomerPaymentProfile)
        controller.execute()

        response = controller.getresponse()

        if response.messages.resultCode == "Ok":
            print(
                "Successfully deleted customer payment profile with customer profile id %s" % deleteCustomerPaymentProfile.customerProfileId)
            models.UserPayments.objects.filter(authorize_net_payment_profile_id=self.kwargs.get('pk')).delete()
        else:
            print(response.messages.message[0]['text'].text)
            print(
                "Failed to delete customer payment profile with customer profile id %s" % deleteCustomerPaymentProfile.customerProfileId)

        return super().get(request, *args, **kwargs)


class AddPaymentBillingView(LoginRequiredMixin, generic.FormView):
    form_class = forms.PaymentBillingForm
    success_url = reverse_lazy("accounts:manage_payment")
    template_name = 'accounts/manage_address_form.html'

    def get_initial(self):
        initial = super(AddPaymentBillingView, self).get_initial()
        initial['country'] = "US"
        return initial

    def form_valid(self, form):
        form.add_billing(self.request.user.authorize_net_profile_id, self.kwargs.get('pk'))
        return super(AddPaymentBillingView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddPaymentBillingView, self).get_context_data(**kwargs)
        number = cart_count(self.request)
        context['number'] = number

        return context


class ManagePaymentView(LoginRequiredMixin, generic.ListView):
    template_name = 'accounts/manage_payment.html'
    default_list = [0]
    payment_list = {}

    def get_queryset(self):
        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = settings.AUTHORIZENET_LOGIN_ID
        merchantAuth.transactionKey = settings.AUTHORIZENET_TRANS_KEY

        getCustomerProfile = apicontractsv1.getCustomerProfileRequest()
        getCustomerProfile.merchantAuthentication = merchantAuth
        getCustomerProfile.customerProfileId = self.request.user.authorize_net_profile_id
        controller = getCustomerProfileController(getCustomerProfile)
        controller.execute()

        response = controller.getresponse()

        if response.messages.resultCode == "Ok":
            if hasattr(response.profile, 'paymentProfiles'):
                for payment in response.profile.paymentProfiles:
                    getCustomerPaymentProfile = apicontractsv1.getCustomerPaymentProfileRequest()
                    getCustomerPaymentProfile.merchantAuthentication = merchantAuth
                    getCustomerPaymentProfile.customerProfileId = self.request.user.authorize_net_profile_id
                    getCustomerPaymentProfile.customerPaymentProfileId = str(payment.customerPaymentProfileId)
                    getCustomerPaymentProfile.unmaskExpirationDate = True

                    controller = getCustomerPaymentProfileController(getCustomerPaymentProfile)
                    controller.execute()

                    response2 = controller.getresponse()

                    if response2.messages.resultCode == "Ok":
                        print("Successfully retrieved a payment profile with profile id %s and customer id %s" % (
                            getCustomerPaymentProfile.customerPaymentProfileId,
                            getCustomerPaymentProfile.customerProfileId))
                        if hasattr(response2, 'paymentProfile'):
                            print(response2.paymentProfile.payment.creditCard.cardNumber)
                            print(response2.paymentProfile.payment.creditCard.expirationDate)

                            if hasattr(response2.paymentProfile, 'defaultPaymentProfile'):
                                if response2.paymentProfile.defaultPaymentProfile:
                                    self.default_list.append(payment.customerPaymentProfileId)
                                    print(len(self.default_list))
                            else:
                                if payment.customerPaymentProfileId in self.default_list:
                                    self.default_list.remove(payment.customerPaymentProfileId)

                            if hasattr(response2.paymentProfile, 'payment'):
                                if hasattr(response2.paymentProfile.payment, 'creditCard'):
                                    self.payment_list[
                                        payment.customerPaymentProfileId] = response2.paymentProfile.payment.creditCard.expirationDate

                    else:
                        print("response code: %s" % response.messages.resultCode)
                        print(
                            "Failed to get payment profile information with id %s" % getCustomerPaymentProfile.customerPaymentProfileId)

                return response.profile.paymentProfiles
        return None

    def get_context_data(self, **kwargs):
        context = super(ManagePaymentView, self).get_context_data(**kwargs)
        number = cart_count(self.request)
        context['number'] = number
        context['default'] = self.default_list
        context['cards'] = self.payment_list
        context['user_payments'] = models.UserPayments.objects.filter(user=self.request.user).all()
        return context
