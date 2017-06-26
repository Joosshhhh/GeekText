from django.contrib.auth.models import AbstractUser
from django.db import models
from books.models import Book


class User(AbstractUser):
    authorize_net_profile_id = models.CharField(max_length=20, null=True)

    def get_full_name(self):
        """
        Returns the firstname plus the lastname, with a space in between.
        """
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def is_active_user(self):
        return self.is_active


class UserPayments(models.Model):
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    card_company = models.CharField(max_length=35, default='Credit')
    authorize_net_payment_profile_id = models.CharField(max_length=35, null=True)
    full_name = models.CharField(max_length=100, null=True)
