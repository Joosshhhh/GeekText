from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.views import generic
from .models import Book, Author, Comment
from cart.views import cart_count
from .forms import CommentForm


class BookListView(generic.ListView):
    template_name = 'book_list.html'
    model = Book

    def get_queryset(self):
        order = self.request.GET.get("sort")
        if order:
            if order == 'rating':
                queryset_list = Book.objects.all().order_by(order).distinct()
            else:
                queryset_list = Book.objects.all().order_by(order)
        else:
            queryset_list = Book.objects.all().order_by("title")

        query = self.request.GET.get("q")  # this gets the contents from the search bar 'q'
        if query:
            queryset_list = queryset_list.filter(title__icontains=query).distinct() | \
                            queryset_list.filter(authors__full_name__icontains=query).distinct() | \
                            queryset_list.filter(genre__icontains=query).distinct()
        return queryset_list

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        queryset_list = self.get_queryset()
        display_sort = self.request.GET.get("display")
        order = self.request.GET.get("sort")
        number = cart_count(self.request)
        context['number'] = number
        context['total'] = self.get_queryset().count()

        if self.request.GET.get("q"):
            context['q'] = self.request.GET.get("q")

        if order:
            context['sort'] = order
            if order == 'title':
                context['sorting'] = "Title - A to Z"
            elif order == '-title':
                context['sorting'] = "Title - Z to A"
            elif order == '-avg_rating':
                context['sorting'] = "Top Rated"
            elif order == 'publication_date':
                context['sorting'] = "Older"
            elif order == '-publication_date':
                context['sorting'] = "Newest"
            elif order == 'authors':
                context['sorting'] = "Author(s) A - Z"
            elif order == '-authors':
                context['sorting'] = "Author(s) Z - A"
            elif order == 'price':
                context['sorting'] = "Price - Low to High"
            elif order == '-price':
                context['sorting'] = "Price - High to Low"
        else:
            context['sort'] = "title"
            context['sorting'] = "Title - A to Z"

        if display_sort:
            if queryset_list.count() > int(display_sort):
                context['display_sort_num'] = display_sort
            else:
                context['display_sort_num'] = display_sort
        else:
            if queryset_list.count() > 10:
                context['display_sort_num'] = 10
            else:
                context['display_sort_num'] = 10

        return context

    def get_paginate_by(self, queryset):
        display_sort = self.request.GET.get("display")
        if display_sort:
            if queryset.count() > int(display_sort):
                paginate_by = display_sort
            else:
                paginate_by = queryset.count()
        else:
            if queryset.count() > 10:
                paginate_by = 10
            else:
                paginate_by = queryset.count()

        return paginate_by


class BookDetailView(generic.DetailView):
    template_name = 'book_detail.html'
    model = Book

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        number = cart_count(self.request)
        context['number'] = number
        author = Author.objects.filter(book=self.kwargs.get("pk")).distinct()
        context['author_books'] = Book.objects.filter(authors__book__authors__in=author).distinct().exclude(
            pk=self.kwargs.get("pk"))
        return context


def list_books(request):
    queryset_list = Book.objects.all().order_by("title")

    query = request.GET.get("q")  # this gets the contents from the search bar 'q'

    if query:
        queryset_list = queryset_list.filter(title__icontains=query).distinct() | \
                        queryset_list.filter(authors__full_name__icontains=query).distinct() | \
                        queryset_list.filter(genre__icontains=query).distinct()

    # creates a Paginator object from the query results and shows x amount of items per page
    paginator = Paginator(queryset_list, 3)  # Show 3 books per page

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

    number_comments = request.POST.get('drop')

    page_req_var = "comment"

    # -- This part deals with how many items on a page based on the dropdown
    if number_comments:
        paginator = Paginator(comments, int(number_comments))
    else:
        paginator = Paginator(comments, 2)
    # ----------------------------------------------------------------------
    page = request.GET.get(page_req_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    number = cart_count(request)

    context = {
        "page_req_var": page_req_var,
        "pages": queryset,
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


def remove_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    id = str(comment.book.id)
    comment.delete()
    return redirect('/book/' + id + '/')


# -----------------------------------------------------------------------------------------


def approve_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    id = str(comment.book.id)
    comment.approve()
    return redirect('/book/' + id + '/')


def paginate(paginate_num, page, queryset):
    paginator = Paginator(queryset, paginate_num)  # Show 25 contacts per page

    page = page
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        books = paginator.page(paginator.num_pages)

    return books
