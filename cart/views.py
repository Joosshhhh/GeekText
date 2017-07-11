from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from books.models import Book
from datetime import *


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

def change_quantity(request):
    book_id = request.POST['book_id']
    quantity = request.POST.get("quantity")
    print("this is book id ", book_id)
    print("this is q ", quantity)

    cart_items = request.session.get('cart', {}).values()  # fetches the values stored in the session

    number = cart_count(request)

    total, book_list = create_list(cart_items, book_id, quantity)

    if total > 0:
        comparison = True
    else:
        comparison = False

    context = {
        "cart": book_list,
        "total": total,
        "number": number,
        "comparison": comparison
    }
    return render(request, "cart_view.html", context)


def view_cart(request):
    cart_items = request.session.get('cart', {}).values()  # fetches the values stored in the session

    number = cart_count(request)

    total, book_list = create_list(cart_items, None, None)

    if total > 0:
        comparison = True
    else:
        comparison = False

    context = {
        "cart": book_list,
        "total": total,
        "number": number,
        "comparison": comparison
    }
    return render(request, "cart_view.html", context)


# -----------------------------------------------------------------------------------------


def remove_item(request, id):
    cart = request.session.get('cart', {})
    del cart[id]
    request.session.modified = True  # this lets the session save correctly

    cart_items = cart.values()

    number = len(cart_items)

    total, book_list = create_list(cart_items, None, 1)

    if total > 0:
        comparison = True
    else:
        comparison = False

    context = {
        "cart": book_list,
        "total": total,
        "number": number,
        "comparison": comparison
    }
    return render(request, "cart_view.html", context)


# -----------------------------------------------------------------------------------------


def checkout(request):
    cart_items = request.session.get('cart', {}).values()
    shipping_tokens = request.POST.get('shipng').split()
    number = cart_count(request)

    total, book_list = create_list(cart_items)

    total = round(float(total), 2)
    shipping = round(float(shipping_tokens[0]), 2)
    subtotal = round(shipping + total, 2)
    tax = round((subtotal * 7) / 100, 2)
    grand_total = round(subtotal + tax, 2)

    code, dates = decode_shipping(shipping_tokens[1])

    context = {
        "number": number,
        "total": total,
        "dates": dates,
        "tax": tax,
        "grandTotal": grand_total,
        "subtotal": subtotal,
        "shipping": shipping,
        "ship_option": code,
    }

    return render(request, "cart_checkout.html", context)


# -----------------------------------------------------------------------------------------

#  ---helper function---
#  takes in a dictionary and creates a list of Book objects into a list
#  also add up the total of the books in the list


def create_list(cart_items, book_id, quantity):

    total = 0
    book_list = []  # holds the list of the books in the cart
    all_books = Book.objects.all()

    for book in cart_items:
        bk = all_books.get(title=book)
        book_price = float(bk.price)

        if book_id:
            if int(book_id) == int(bk.id):
                total = total + book_price * float(quantity)

            else:
                total = total + book_price

        else:
            total = total + book_price

        book_list.append(bk)

    return total, book_list


# -----------------------------------------------------------------------------------------


def cart_count(request):
    cart = request.session.get('cart', {})
    cart_items = cart.values()  # fetches the values stored in the session

    number = len(cart_items)  # this is used to display the number of items in the cart

    return number


# -----------------------------------------------------------------------------------------
# ---Helper function below, reads in input from a radio option where it decodes and calculates the
# estimated delivery date along with the Shipping option


def decode_shipping(code):
    dates = datetime.today()

    output = ''

    if code == '-T-':
        output = 'Two-Day Shipping (2 Business Days)'
        dates = dates + timedelta(days=2)
    elif code == '-R-':
        output = 'Regular Shipping (3-5 Business Days)'
        dates = dates + timedelta(days=5)
    elif code == '-N-':
        output = 'Next-Day Shipping (1 Business Day)'
        dates = dates + timedelta(days=1)

    return output, dates

# -----------------------------------------------------------------------------------------

