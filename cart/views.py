from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from books.models import Book

# Create your views here.


def add_cart(request, id):

    book = get_object_or_404(Book, id=id)

    cart = request.session.get('cart', {})
    cart[id] = book.title
    request.session['cart'] = cart

    number = cart_count(request)

    messages.success(request, "'" + book.title + "' has been added to your cart!")

    context = {
        "book": book,
        "number": number,
    }

    return render(request, "cart_home.html", context)
# -----------------------------------------------------------------------------------------


def view_cart(request):

    cart_items = request.session.get('cart', {}).values()  # fetches the values stored in the session

    number = cart_count(request)

    total, book_list = create_list(cart_items)

    context = {
        "cart": book_list,
        "total": total,
        "number": number,
    }
    return render(request, "cart_view.html", context)

# -----------------------------------------------------------------------------------------


def remove_item(request, id):

    cart = request.session.get('cart', {})

    del cart[id]
    request.session.modified = True  # this lets the session save correctly

    cart_items = cart.values()

    number = len(cart_items)

    total, book_list = create_list(cart_items)

    context = {
        "cart": book_list,
        "total": total,
        "number": number,
    }
    return render(request, "cart_view.html", context)


def checkout(request):

    number = cart_count(request)

    context = {
        "number": number,
    }

    return render(request, "cart_checkout.html", context)

# -----------------------------------------------------------------------------------------

#  ---helper function---
#  takes in a dictionary and creates a list of Book objects into a list


def create_list(cart_items):

    total = 0
    book_list = []  # holds the list of the books in the cart
    all_books = Book.objects.all()

    for book in cart_items:
        bk = all_books.get(title=book)
        book_list.append(bk)
        total = total + bk.price

    return total, book_list
# -----------------------------------------------------------------------------------------


def cart_count(request):

    cart = request.session.get('cart', {})
    cart_items = cart.values()  # fetches the values stored in the session

    number = len(cart_items)  # this is used to display the number of items in the cart

    return number
