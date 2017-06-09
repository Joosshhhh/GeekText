from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .models import Book

from . import forms, models


# Create your views here.

def list_books(request):

    queryset_list = Book.objects.all().order_by("title")

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(title__icontains=query)

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
        "results": queryset,
        "title": "Results",
        "page_req_var": page_req_var,
    }
    return render(request, "book_list.html", context)


def detail(request, id):
    target = get_object_or_404(Book, id=id)
    context = {
        "result": target,
    }
    return render(request, "book_detail.html", context)




