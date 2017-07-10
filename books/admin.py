# Register your models here.

from django.contrib import admin
from .models import Publisher, Author, Book, Comment


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email')
    search_fields = ('full_name', 'email')


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'publisher', 'publication_date')
    list_filter = ('publication_date',)
    date_hierarchy = 'publication_date'
    ordering = ('-publication_date',)
    raw_id_fields = ('publisher',)


admin.site.register(Publisher)
admin.site.register(Comment)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
