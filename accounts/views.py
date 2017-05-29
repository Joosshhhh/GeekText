from authorizenet.apicontrollers import *
from django import forms
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.urlresolvers import reverse_lazy
from django.views import generic

from . import forms


class RegisterView(generic.CreateView):
    form_class = forms.Register
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/register.html"


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


class ManageAccountView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/manage.html'


class AccountUpdateAvatarView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.AccountUpdateFirstName
    success_url = reverse_lazy("accounts:manage_profile")
    template_name = 'accounts/profile/manage_avatar.html'

    def get_object(self, queryset=None):
        return self.request.user


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


class ManageProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/manage_profile.html'


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
                                self.default_list[0] = address.customerAddressId
                                print(len(self.default_list))
                        else:
                            if address.customerAddressId in self.default_list:
                                del self.default_list[0]
                    else:
                        print("ERROR")
                        print("Message text : %s " % response.messages.message[0]['text'].text)

                else:
                    print("No addresses yet")

                return response.profile.shipToList

        return None

    def get_context_data(self, **kwargs):
        context = super(ManageAddressView, self).get_context_data(**kwargs)
        context['default'] = self.default_list
        return context


class PaymentAddView(LoginRequiredMixin, generic.FormView):
    form_class = forms.UserPaymentForm
    success_url = reverse_lazy("accounts:manage_payment")
    template_name = "accounts/manage_payment_form.html"

    def form_valid(self, form):

        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = settings.AUTHORIZENET_LOGIN_ID
        merchantAuth.transactionKey = settings.AUTHORIZENET_TRANS_KEY
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
                    response = getShippingAddressController.getresponse()

                    if response.messages.resultCode == "Ok":
                        print("SUCCESS")
                        if hasattr(response, 'defaultShippingAddress'):
                            if response.defaultShippingAddress:
                                billTo.firstName = response.address.firstName
                                billTo.lastName = response.address.lastName
                                billTo.address = response.address.address
                                billTo.city = response.address.city
                                billTo.state = response.address.state
                                billTo.zip = response.address.zip
                                billTo.country = response.address.country
                                billTo.phoneNumber = str(response.address.phoneNumber)
                    else:
                        print("ERROR")
                        print("Message text : %s " % response.messages.message[0]['text'].text)
            else:
                print('No shipping addresses')
        else:
            print("ERROR")
            print("Message text : %s " % response.messages.message[0]['text'].text)

        profile = apicontractsv1.customerPaymentProfileType()
        profile.payment = payment
        profile.billTo = billTo
        profile.customerType = 'individual'
        profile.defaultPaymentProfile = form.cleaned_data['default']

        createCustomerPaymentProfile = apicontractsv1.createCustomerPaymentProfileRequest()
        createCustomerPaymentProfile.merchantAuthentication = merchantAuth
        createCustomerPaymentProfile.paymentProfile = profile
        createCustomerPaymentProfile.customerProfileId = self.request.user.authorize_net_profile_id
        createCustomerPaymentProfile.validationMode = 'testMode'

        controller = createCustomerPaymentProfileController(createCustomerPaymentProfile)
        controller.execute()

        response = controller.getresponse()

        if response.messages.resultCode == "Ok":
            print("Successfully created a customer payment profile with id: %s" % response.customerPaymentProfileId)
        else:
            print("ERROR")
            print("Message text : %s " % response.messages.message[0]['text'].text)

        return super(PaymentAddView, self).form_valid(form)


class ManagePaymentView(LoginRequiredMixin, generic.ListView):
    template_name = 'accounts/manage_payment.html'

    def get_queryset(self):
        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = settings.AUTHORIZENET_LOGIN_ID
        merchantAuth.transactionKey = settings.AUTHORIZENET_TRANS_KEY

        getCustomerProfile = apicontractsv1.getCustomerProfileRequest()
        getCustomerProfile.merchantAuthentication = merchantAuth
        getCustomerProfile.customerProfileId = self.request.user.authorize_net_profile_id
        getCustomerProfile.unmaskExpirationDate = True
        controller = getCustomerProfileController(getCustomerProfile)
        controller.execute()

        response = controller.getresponse()

        if response.messages.resultCode == "Ok":
            if hasattr(response.profile, 'paymentProfiles'):
                return response.profile.paymentProfiles
        return None
