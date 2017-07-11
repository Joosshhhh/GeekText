from django.db import models
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.fields import GenericRelation


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
    email = models.EmailField(null=True)
    description = models.TextField(max_length=600, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    birthplace = models.CharField(max_length=75, null=True, blank=True)
    education = models.CharField(max_length=100, null=True, blank=True)
    website = models.URLField(null=True)
    image = models.FileField(null=True, blank=True)

    def __str__(self):
        return u'%s' % self.full_name

    def get_absolute_url(self):
        return "/book/author/%s/" % self.id

    class Meta:
        ordering = ['full_name']


class Book(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(null=True, blank=True)
    authors = models.ManyToManyField(Author)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField(null=True, blank=True, auto_now_add=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=600, null=True, blank=True)
    pages = models.IntegerField(default=0)
    avg_rating = models.DecimalField(decimal_places=1, max_digits=2, default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/book/%s/" % self.id

    def author(self):
        return Author.objects.filter(book__authors__book=self.id).distinct()

    def rating_avg(self):
        book = Book.objects.get(id=self.id)
        return list(book.rating_set.aggregate(Avg('rating')).values())[0]

    def rating_count(self):
        return Rating.objects.all().filter(book=self).count()

    class Meta:
        ordering = ['title']


class Rating(models.Model):
    book = models.ForeignKey(Book)
    rating = models.DecimalField(decimal_places=1, max_digits=2, default=0)

    class Meta:
        ordering = ['-rating']


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
