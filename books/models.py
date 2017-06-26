from django.db import models
from django.shortcuts import get_object_or_404
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
        # this function creates a list of all the authors to later convert them into Author objects
        author_string = ",".join([a.full_name for a in self.authors.all()])
        author_list = []

        tokens = author_string.split(",")

        for token in tokens:
            author_list.append(get_object_or_404(Author, full_name=token))

        return author_list

    class Meta:
        ordering = ['title']


class Comment(models.Model):
    book = models.ForeignKey(Book)
    author = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateField()
    approved = models.BooleanField(default=False)

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):

        return self.book.title

    class Meta:
        ordering = ['-date']