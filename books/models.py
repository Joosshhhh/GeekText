from django.db import models

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
    full_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return u'%s' % self.full_name

    def get_absolute_url(self):
        return "/book/author/%s/" % self.id

    def get_titles(self):
        return ",\n".join([book.title for book in self.book_set.all()])

    class Meta:
        ordering = ['full_name']


class Book(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(null=True, blank=True)
    authors = models.ManyToManyField(Author)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField()
    genre = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=600, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/book/%s/" % self.id

    def author(self):
        return ",\n".join([a.full_name for a in self.authors.all()])

    class Meta:
        ordering = ['title']


