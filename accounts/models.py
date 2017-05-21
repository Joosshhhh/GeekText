from django.contrib.auth.models import AbstractUser
from django.db import models

US_STATES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)


class User(AbstractUser):
    #   avatar = models.ImageField();
    #   if we do this remember to migrate
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
    address = models.CharField(max_length=120)
    address2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120, choices=US_STATES, null=True, blank=True)
    country = models.CharField(max_length=120)
    zipcode = models.CharField(max_length=25)
    phone = models.CharField(max_length=120)
    shipping = models.BooleanField(default=True)
    billing = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.get_address()

    def get_address(self):
        return "{}, {}, {}, {}, {}".format(self.address, self.city, self.state, self.country, self.zipcode)

    objects = UserAddressManager()

    class Meta:
        ordering = ['-updated', '-timestamp']
