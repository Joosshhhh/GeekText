from django.views import generic
from books.models import Book
from django.shortcuts import render


class HomeView(generic.TemplateView):
    template_name = 'home.html'


def home_view(request):
    books = Book.objects.all().order_by("title")
    cart = request.session.get('cart', {})
    number = len(cart.values())
    context = {
        "books": books,
        "number": number,
    }
    return render(request, "home.html", context)
