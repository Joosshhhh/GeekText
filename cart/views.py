from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from books.models import Book

# Create your views here.


def cart_home(request):

    return render(request, "cart_home.html")
# -----------------------------------------------------------------------------------------


def add_cart(request, id):

    book = get_object_or_404(Book, id=id)

    cart = request.session.get('cart', {})
    cart[id] = book.title
    request.session['cart'] = cart

    messages.success(request, "'" + book.title + "' has been added to your cart!")

    context = {
        "book": book,
    }

    return render(request, "cart_home.html", context)
# -----------------------------------------------------------------------------------------


def view_cart(request):

    book_list = []  # holds the list of the books in the cart
    total = 0

    all_books = Book.objects.all()

    cart = request.session.get('cart', {})
    cart_items = cart.values()  # fetches the values stored in the session

    number = len(cart_items)  # this is used to display the number of items in the cart

    #  this for loop creates a list of Book objects that were gathered from the session
    # (creates the shopping cart)
    for book in cart_items:
        bk = all_books.get(title=book)
        book_list.append(bk)
        total = total + bk.price

    context = {
        "cart": book_list,
        "total": total,
        "number": number,
    }
    return render(request, "cart_checkout.html", context)

# -----------------------------------------------------------------------------------------


def remove_item(request, id):

    book_list = []  # holds the list of the books in the cart
    all_books = Book.objects.all()
    total = 0

    cart = request.session.get('cart', {})

    del cart[id]
    request.session.modified = True  # this lets the session save correctly

    cart_items = cart.values()
    number = len(cart_items)

    for book in cart_items:
        bk = all_books.get(title=book)
        book_list.append(bk)
        total = total + bk.price

    context = {
        "cart": book_list,
        "total": total,
        "number": number,
    }
    return render(request, "cart_checkout.html", context)
# -----------------------------------------------------------------------------------------
