from django.contrib.auth.models import AbstractUser


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
