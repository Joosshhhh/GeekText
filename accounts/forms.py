from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django_countries import countries

from .models import UserAddress

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
        user_count = User.objects.filter(email=email).count()
        if user_count > 0:
            raise forms.ValidationError(
                "This email has already been registered. Please check and try again or reset your password.")
        return email

    def save(self, commit=True):
        user = super(Register, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
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
        if confirm and new_email != confirm:
            raise forms.ValidationError(
                'Email fields must match'
            )
        return new_email


class AccountUpdateUsername(forms.ModelForm):
    username = forms.CharField(max_length=20, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))

    class Meta:
        fields = ["username"]
        model = User


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


class UserAddressForm(forms.ModelForm):
    full_name = forms.CharField(max_length=75,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}))
    address = forms.CharField(max_length=120,
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control', 'placeholder': 'Street and number, P.O. box'}))
    address2 = forms.CharField(max_length=120, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Apartment, suite, unit, '
                                                                            'building, floor, etc.'}))
    city = forms.CharField(max_length=120,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    state = forms.CharField(max_length=120,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    country = forms.TypedChoiceField(choices=countries,
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    zipcode = forms.CharField(max_length=25,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}))
    phone = forms.CharField(max_length=120,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}))

    class Meta:
        model = UserAddress
        fields = ["full_name",
                  "address",
                  "address2",
                  "city",
                  "state",
                  "country",
                  "zipcode",
                  "phone"]

        # def clean(self):
        #     # check address via some self-defined helper function
        #     auth_id = settings.SMARTY_AUTH_ID  # We recommend storing your keys in environment variables
        #     auth_token = settings.SMARTY_AUTH_TOKEN
        #     credentials = StaticCredentials(auth_id, auth_token)
        #     client = ClientBuilder(credentials).build_international_street_api_client()
        #     if self.cleaned_data.get('address2'):
        #         address = self.cleaned_data['address'] + ' ' + self.cleaned_data.get(
        #             'address2') + ', ' + self.cleaned_data.get(
        #             'city')
        #     else:
        #         address = self.cleaned_data['address'] + ', ' + self.cleaned_data.get(
        #             'city')
        #     lookup = Lookup(address, self.cleaned_data.get('country'))
        #     lookup.geocode = True  # Must be expressly set to get latitude and longitude.
        #
        #     candidates = client.send(lookup)  # The candidates are also stored in the lookup's 'result' field.
        #     if not candidates:
        #         raise forms.ValidationError("Your address couldn't be found...")
        #     elif len(candidates) > 1:
        #         raise forms.ValidationError('Did you mean...')
