import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.views import generic
from .models import Book, Author, Comment
from cart.views import cart_count
from .forms import CommentForm


class AllAuthorsView(generic.TemplateView):
    template_name = 'book_author.html'

    def get_context_data(self, **kwargs):
        context = super(AllAuthorsView, self).get_context_data(**kwargs)
        context['a'] = Author.objects.filter(full_name__startswith="A")
        context['b'] = Author.objects.filter(full_name__startswith="B")
        context['c'] = Author.objects.filter(full_name__startswith="C")
        context['d'] = Author.objects.filter(full_name__startswith="D")
        context['e'] = Author.objects.filter(full_name__startswith="E")
        context['f'] = Author.objects.filter(full_name__startswith="F")
        context['g'] = Author.objects.filter(full_name__startswith="G")
        context['h'] = Author.objects.filter(full_name__startswith="H")
        context['i'] = Author.objects.filter(full_name__startswith="I")
        context['j'] = Author.objects.filter(full_name__startswith="J")
        context['k'] = Author.objects.filter(full_name__startswith="K")
        context['l'] = Author.objects.filter(full_name__startswith="L")
        context['m'] = Author.objects.filter(full_name__startswith="M")
        context['n'] = Author.objects.filter(full_name__startswith="N")
        context['o'] = Author.objects.filter(full_name__startswith="O")
        context['p'] = Author.objects.filter(full_name__startswith="P")
        context['q'] = Author.objects.filter(full_name__startswith="Q")
        context['r'] = Author.objects.filter(full_name__startswith="R")
        context['s'] = Author.objects.filter(full_name__startswith="S")
        context['t'] = Author.objects.filter(full_name__startswith="T")
        context['u'] = Author.objects.filter(full_name__startswith="U")
        context['v'] = Author.objects.filter(full_name__startswith="V")
        context['w'] = Author.objects.filter(full_name__startswith="W")
        context['x'] = Author.objects.filter(full_name__startswith="X")
        context['y'] = Author.objects.filter(full_name__startswith="Y")
        context['z'] = Author.objects.filter(full_name__startswith="Z")
        return context


class BookListView(generic.ListView):
    template_name = 'book_list.html'
    model = Book

    def get_queryset(self):
        order = self.request.GET.get("sort")
        order2 = self.request.GET.get("order")
        queryset_list = Book.objects.all()

        query = self.request.GET.get("q")  # this gets the contents from the search bar 'q'
        if query:
            if query in 'Tech Valley Times Best Sellers':
                queryset_list = queryset_list.filter(tech_valley_best=1)
            elif query in 'Coming Soon':
                queryset_list = queryset_list.filter(publication_date__gt=datetime.date.today())
            elif 'Star' in query:
                if 'One' in query:
                    queryset_list = queryset_list.filter(avg_rating__range=(1, 1.9))
                elif 'Two' in query:
                    queryset_list = queryset_list.filter(avg_rating__range=(2, 2.9))
                elif 'Three' in query:
                    queryset_list = queryset_list.filter(avg_rating__range=(3, 3.9))
                elif 'Four' in query:
                    queryset_list = queryset_list.filter(avg_rating__range=(4, 4.5))
                elif 'Five' in query:
                    queryset_list = queryset_list.filter(avg_rating__range=(4.6, 5))

            else:
                queryset_list = queryset_list.filter(title__icontains=query).distinct() | \
                                queryset_list.filter(authors__full_name__icontains=query).distinct() | \
                                queryset_list.filter(genre__icontains=query).distinct()

        if order:
            if query and order2 and queryset_list.filter(genre__icontains=query):
                queryset_list = queryset_list.order_by(order, order2)
            else:
                if order == 'sales_rank':
                    queryset_list = queryset_list.order_by(order).exclude(sales_rank=0)
                else:
                    queryset_list = queryset_list.order_by(order)
        else:
            if query and order2 and queryset_list.filter(genre__icontains=query):
                queryset_list = queryset_list.order_by("-tech_valley_best", order2)
            else:
                queryset_list = queryset_list.order_by("title")

        return queryset_list

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        queryset_list = self.get_queryset()
        display_sort = self.request.GET.get("display")
        order = self.request.GET.get("sort")
        order2 = self.request.GET.get("order")
        number = cart_count(self.request)
        context['number'] = number
        context['total'] = self.get_queryset().count()
        query = self.request.GET.get("q")

        if query:
            context['q'] = query

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
            elif order == 'sales_rank':
                context['sorting'] = "Top Sellers"
            elif order == '-tech_valley_best':
                context['sorting'] = "Tech Valley Best Sellers"
        else:
            if query and Book.objects.filter(genre__icontains=query):
                context['sort'] = "-tech_valley_best"
                context['order'] = "-rating"
                context['sorting'] = "Tech Valley Best Sellers"
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

        if order2:
            context['order'] = order2

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
