from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Book, Author


def list_books(request):

    queryset_list = Book.objects.all().order_by("title")
    queryset_author = Author.objects.all().order_by("last_name")

    query = request.GET.get("q")

    if query:
        queryset_list = queryset_list.filter(title__icontains=query).distinct() | \
                        queryset_list.filter(authors__full_name__icontains=query).distinct() | \
                        queryset_list.filter(genre__icontains=query).distinct()

    paginator = Paginator(queryset_list, 25)  # Show 25 contacts per page

    page_req_var = "page"

    page = request.GET.get(page_req_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "author": queryset_author,
        "results": queryset,
        "title": "Displaying all Books",
        "page_req_var": page_req_var,
    }
    return render(request, "book_list.html", context)


def detail(request, id):

    book = get_object_or_404(Book, id=id)
    context = {
        "result": book,
    }
    return render(request, "book_detail.html", context)


def author_books(request, id):

    author = get_object_or_404(Author, id=id)
    books = author.get_titles()
    context = {
        "author": author,
        "books": books
    }
    return render(request, "book_author.html", context)
