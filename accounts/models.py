from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField


class User(AbstractUser):
    # avatar = models.ImageField(upload_to="photos/", null=True, blank=True)

    def get_full_name(self):
        """
        Returns the firstname plus the lastname, with a space in between.
        """
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name


class UserDefaultAddress(models.Model):
    user = models.OneToOneField(User)
    shipping = models.ForeignKey("UserAddress", null=True,
                                 blank=True, related_name="user_address_shipping_default")
    billing = models.ForeignKey("UserAddress", null=True,
                                blank=True, related_name="user_address_billing_default")

    def __str__(self):
        return self.user.username


class UserAddressManager(models.Manager):
    def get_billing_addresses(self, user):
        return super(UserAddressManager, self).filter(billing=True).filter(user=user)


class UserAddress(models.Model):
    user = models.ForeignKey(User)
    full_name = models.CharField(max_length=70)
    address = models.CharField(max_length=120)
    address2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120, null=True, blank=True)
    country = CountryField()
    zipcode = models.CharField(max_length=25)
    phone = models.CharField(max_length=120)
    shipping = models.BooleanField(default=True)
    billing = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.get_address()

    def get_address(self):
        return "{}, {}, {}, {}, {}".format(self.full_name, self.address, self.city, self.state, self.country,
                                           self.zipcode)

    objects = UserAddressManager()

    class Meta:
        ordering = ['-updated', '-timestamp']
