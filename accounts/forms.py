from authorizenet.apicontrollers import *
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django_countries import countries

User = get_user_model()


class Register(UserCreationForm):
    first_name = forms.CharField(max_length=35,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=35,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))
    username = forms.CharField(max_length=20,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        fields = ("email", "first_name", "last_name", "username", "password1")
        model = User

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email has already been registered. Please check and try again or reset your password.")
        return email

    def save(self, commit=True):
        user = super(Register, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = settings.AUTHORIZENET_LOGIN_ID
        merchantAuth.transactionKey = settings.AUTHORIZENET_TRANS_KEY

        createCustomerProfile = apicontractsv1.createCustomerProfileRequest()
        createCustomerProfile.merchantAuthentication = merchantAuth
        createCustomerProfile.profile = apicontractsv1.customerProfileType(self.cleaned_data['username'], 'New user',
                                                                           self.cleaned_data['email'])

        controller = createCustomerProfileController(createCustomerProfile)
        controller.execute()

        response = controller.getresponse()
        if response.messages.resultCode != "Ok":
            raise forms.ValidationError(
                "Sorry couldn't create customer profile"
            )
        else:
            user.authorize_net_profile_id = response.customerProfileId

        if commit:
            user.save()

        return user


class Login(AuthenticationForm):
    username = forms.CharField(max_length=20,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class AccountUpdateFirstName(forms.ModelForm):
    first_name = forms.CharField(max_length=35, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))

    class Meta:
        fields = ["first_name"]
        model = User


class AccountUpdateLastName(forms.ModelForm):
    last_name = forms.CharField(max_length=35, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))

    class Meta:
        fields = ["last_name"]
        model = User


class AccountUpdateEmail(forms.ModelForm):
    email = forms.EmailField(required=False,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    email_confirm = forms.EmailField(required=False,
                                     widget=forms.EmailInput(
                                         attrs={'class': 'form-control', 'placeholder': 'Confirm New Email'}))

    class Meta:
        fields = ["email"]
        model = User

    def clean_email(self):
        new_email = self.cleaned_data.get('email')
        confirm = self.cleaned_data.get('email_confirm')

        if confirm and new_email and new_email != confirm:
            raise forms.ValidationError(
                'Email fields must match'
            )
        if User.objects.filter(email=confirm).exists():
            raise forms.ValidationError(
                'This email has already been taken. Please try another.'
            )
        return new_email


class AccountUpdateUsername(forms.ModelForm):
    username = forms.CharField(max_length=20, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))

    class Meta:
        fields = ["username"]
        model = User

    def clean_username(self):
        new_username = self.cleaned_data.get('username')
        if User.objects.filter(username=new_username).exists():
            raise forms.ValidationError(
                'This username has already been taken. Please try another.'
            )


class AccountUpdatePassword(PasswordChangeForm):
    old_password = forms.CharField(required=False, strip=False,
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control', 'placeholder': 'Old Password',
                                              'autofocus': True}))
    new_password1 = forms.CharField(required=False, strip=False,
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    new_password2 = forms.CharField(required=False, strip=False,
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}))


class DeactivateForm(forms.ModelForm):
    deactivate = forms.BooleanField(widget=forms.CheckboxInput, label='Deactivate Account MUTHAFUCKA')

    class Meta:
        model = User
        fields = ['is_active']

    def save(self, commit=True):
        user = super(DeactivateForm, self).save(commit=False)
        if self.cleaned_data.get('deactivate'):
            user.is_active = False
        if commit:
            user.save()
        return user


class UserAddressForm(forms.Form):
    first_name = forms.CharField(max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))
    address = forms.CharField(max_length=60,
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control', 'placeholder': 'Street and number, P.O. box'}))
    address2 = forms.CharField(max_length=60, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Apartment, suite, unit, '
                                                                            'building, floor, etc.'}))
    city = forms.CharField(max_length=40,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    state = forms.CharField(max_length=40,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    country = forms.TypedChoiceField(choices=countries,
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    zipcode = forms.CharField(max_length=20,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}))
    phone = forms.CharField(max_length=25,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}))
    default = forms.BooleanField(label='Set as default', required=False)

    def add_shipping_address(self, authorizenet_id):

        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = settings.AUTHORIZENET_LOGIN_ID
        merchantAuth.transactionKey = settings.AUTHORIZENET_TRANS_KEY

        # Give address details
        officeAddress = apicontractsv1.customerAddressType()
        officeAddress.firstName = self.cleaned_data['first_name']
        officeAddress.lastName = self.cleaned_data['last_name']
        officeAddress.address = self.cleaned_data['address']
        officeAddress.city = self.cleaned_data['city']
        officeAddress.state = self.cleaned_data['state']
        officeAddress.zip = self.cleaned_data['zipcode']
        officeAddress.country = self.cleaned_data['country']
        officeAddress.phoneNumber = self.cleaned_data['phone']

        # Create shipping address request
        shippingAddressRequest = apicontractsv1.createCustomerShippingAddressRequest()
        shippingAddressRequest.address = officeAddress
        shippingAddressRequest.customerProfileId = authorizenet_id
        shippingAddressRequest.defaultShippingAddress = self.cleaned_data['default']
        shippingAddressRequest.merchantAuthentication = merchantAuth

        # Make an API call
        controller = createCustomerShippingAddressController(shippingAddressRequest)
        controller.execute()
        response = controller.getresponse()

        if response.messages.resultCode == "Ok":
            print("SUCCESS")
            print("Customer address id : %s" % response.customerAddressId)
        else:
            raise forms.ValidationError(
                "Message text : %s " % response.messages.message[0]['text'].text
            )

    def update_shipping_address(self, authorizenet_id, authorizenet_address_id):

        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = settings.AUTHORIZENET_LOGIN_ID
        merchantAuth.transactionKey = settings.AUTHORIZENET_TRANS_KEY

        # Give updated address details
        officeAddress = apicontractsv1.customerAddressExType()
        officeAddress.firstName = self.cleaned_data['first_name']
        officeAddress.lastName = self.cleaned_data['last_name']
        officeAddress.address = self.cleaned_data['address']
        officeAddress.city = self.cleaned_data['city']
        officeAddress.state = self.cleaned_data['state']
        officeAddress.zip = self.cleaned_data['zipcode']
        officeAddress.country = self.cleaned_data['country']
        officeAddress.phoneNumber = self.cleaned_data['phone']
        officeAddress.customerAddressId = authorizenet_address_id

        # Create update shipping address request
        updateShippingAddressRequest = apicontractsv1.updateCustomerShippingAddressRequest()
        updateShippingAddressRequest.address = officeAddress
        updateShippingAddressRequest.customerProfileId = authorizenet_id
        updateShippingAddressRequest.merchantAuthentication = merchantAuth
        updateShippingAddressRequest.defaultShippingAddress = self.cleaned_data['default']

        # Make the API call
        updateShippingAddressController = updateCustomerShippingAddressController(updateShippingAddressRequest)
        updateShippingAddressController.execute()
        response = updateShippingAddressController.getresponse()

        if response.messages.resultCode == "Ok":
            print("SUCCESS")
            print("Message text : %s " % response.messages.message[0]['text'].text)
        else:
            raise forms.ValidationError(
                "Message text : %s " % response.messages.message[0]['text'].text
            )


class UserPaymentForm(forms.Form):
    card_first = forms.CharField(max_length=4,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'placeholder': '0000'}))
    card_second = forms.CharField(max_length=4,
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control', 'placeholder': '0000'}))
    card_third = forms.CharField(max_length=4,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'placeholder': '0000'}))
    card_fourth = forms.CharField(max_length=4,
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control', 'placeholder': '0000'}))
    ccv = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CCV'}))
    exp_month = forms.CharField(max_length=2,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM'}))
    exp_year = forms.CharField(max_length=4,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YYYY'}))
    full_name = forms.CharField(max_length=75,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Name On The Card'}))
    default = forms.BooleanField(label='Set as default', required=False)
