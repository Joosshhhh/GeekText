from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from .models import Book, Author, Comment
from cart.views import cart_count
from .forms import CommentForm


def list_books(request):

    queryset_list = Book.objects.all().order_by("title")

    query = request.GET.get("q")

    if query:
        queryset_list = queryset_list.filter(title__icontains=query).distinct() | \
                        queryset_list.filter(authors__full_name__icontains=query).distinct() | \
                        queryset_list.filter(genre__icontains=query).distinct()

    paginator = Paginator(queryset_list, 5)  # Show 25 contacts per page

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

    if query:
        query = query
    else:
        query = "Books"

    number = cart_count(request)

    context = {
        "search": query,
        "results": queryset,
        "title": "Displaying all Results for: ",
        "page_req_var": page_req_var,
        "number": number,
    }
    return render(request, "book_list.html", context)
# -----------------------------------------------------------------------------------------


def detail(request, id):

    book = get_object_or_404(Book, id=id)
    comments = Comment.objects.filter(book__title=book.title)

    number = cart_count(request)

    context = {
        "comments": comments,
        "result": book,
        "number": number,
    }
    return render(request, "book_detail.html", context)
# -----------------------------------------------------------------------------------------


def author_books(request, id):

    author = get_object_or_404(Author, id=id)
    books = Book.objects.all().filter(authors__full_name__icontains=author)
    number = cart_count(request)

    context = {
        "author": author,
        "books": books,
        "number": number
    }
    return render(request, "book_author.html", context)
# -----------------------------------------------------------------------------------------


def write_review(request, id):

    number = cart_count(request)
    book = get_object_or_404(Book, id=id)

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.book = book
            comment.author = request.user
            comment.date = timezone.now()
            comment.save()

            return redirect('/book/' + id + '/')
    else:
        form = CommentForm()

    context = {
        "number": number,
        "book": book,
        "form": form
    }

    return render(request, "book_review.html", context)
# -----------------------------------------------------------------------------------------
