from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.


class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()

    def __str__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    class Meta:
        ordering = ['first_name', 'last_name']


class Book(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(null=True, blank=True)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField()
    genre = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=600, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/book/%s/" % self.id

    def author(self):
        return ",\n".join([a.first_name + " " + a.last_name for a in self.authors.all()])

    class Meta:
        ordering = ['title']



