from django.views import generic
from books.models import Book
from django.shortcuts import render
from cart.views import cart_count


class HomeView(generic.TemplateView):
    template_name = 'home.html'


def home_view(request):
    books = Book.objects.all().order_by("title")

    number = cart_count(request)

    context = {
        "books": books,
        "number": number,
    }
    return render(request, "home.html", context)
