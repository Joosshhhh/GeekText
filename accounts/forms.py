from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import UserAddress

User = get_user_model()


class Register(UserCreationForm):
    first_name = forms.CharField(max_length=35,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=35,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))
    username = forms.CharField(max_length=40,
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
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


# Handle the update logic here
#   I just copied it from Register
#   Somehow have to only update the fields the user filled out
class AccountUpdateProfile(forms.ModelForm):
    first_name = forms.CharField(max_length=35, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=35, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))
    username = forms.CharField(max_length=40, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(required=False,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    email_confirm = forms.EmailField(required=False,
                                     widget=forms.EmailInput(
                                         attrs={'class': 'form-control', 'placeholder': 'Confirm Email'}))
    old_password = forms.CharField(required=False, strip=False,
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control', 'placeholder': 'Old Password'}))
    password = forms.CharField(required=False, strip=False,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    password2 = forms.CharField(required=False, strip=False,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}))
    middle_name = forms.CharField(validators=[''])

    class Meta:
        fields = ("first_name", "last_name", "username", "email", "password")
        model = User

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_confirm = self.cleaned_data.get("email_confirm")
        if email and email_confirm and email != email_confirm:
            raise forms.ValidationError(
                "Email fields don't match.")
        return email

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if old_password and not self.instance.check_password(old_password):
            raise forms.ValidationError(
                "Old password is incorrect."
            )
        return old_password

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        old_password = self.cleaned_data.get('old_password')

        if password and password2:
            if not old_password:
                raise forms.ValidationError(
                    "Must enter your current password."
                )
            if password != password2:
                raise forms.ValidationError(
                    "The new password fields must match."
                )
            password_validation.validate_password(password, self.instance)
        return password

    def save(self, commit=True):
        user = super(AccountUpdateProfile, self).save(commit=False)
        if self.instance.password != self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class DeactivateForm(forms.ModelForm):
    deactivate = forms.BooleanField(widget=forms.CheckboxInput, label='Deactivate Account MUTHAFUCKA')

    class Meta:
        model = User
        fields = ['is_active']


class UserAddressForm(forms.ModelForm):
    default = forms.BooleanField(label='Make Default')

    class Meta:
        model = UserAddress
        fields = ["address",
                  "address2",
                  "city",
                  "state",
                  "country",
                  "zipcode",
                  "phone"]
