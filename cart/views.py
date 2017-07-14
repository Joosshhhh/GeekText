from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from books.models import Book
from datetime import *


def add_cart(request, id):
    book = get_object_or_404(Book, id=id)

    request.session[id] = 1

    cart = request.session.get('cart', {})
    cart[id] = book.title
    request.session['cart'] = cart

    number = cart_count(request)

    messages.success(request, "'" + book.title + "' has been added to your cart!")

    context = {
        "book": book,
        "number": number,
        "request": request
    }

    return render(request, "cart_home.html", context)


# -----------------------------------------------------------------------------------------

def change_quantity(request):
    book_id = request.POST.get("book_id")
    quantity = request.POST.get("quantity")

    cart_items = request.session.get('cart', {}).values()  # fetches the values stored in the session
    number = cart_count(request)

    total, book_list = create_list(cart_items, book_id, quantity, request)
    request.session['total'] = total

    if total > 0:
        comparison = True
    else:
        comparison = False

    context = {
        "cart": book_list,
        "total": total,
        "number": number,
        "comparison": comparison,
        "request": request
    }
    return render(request, "cart_view.html", context)

# -----------------------------------------------------------------------------------------


def view_cart(request):
    cart_items = request.session.get('cart', {}).values()  # fetches the values stored in the session

    number = cart_count(request)

    total, book_list = create_list(cart_items, None, 1, request)

    request.session['total'] = total

    if total > 0:
        comparison = True
    else:
        comparison = False

    context = {
        "cart": book_list,
        "total": total,
        "number": number,
        "comparison": comparison,
        "request": request,
    }
    return render(request, "cart_view.html", context)


# -----------------------------------------------------------------------------------------


def remove_item(request, id):

    cart = request.session.get('cart', {})

    del cart[id]
    request.session.modified = True  # this lets the session save correctly

    cart_items = cart.values()

    number = len(cart_items)

    total, book_list = create_list(cart_items, None, 1, request)

    request.session['total'] = total

    if total > 0:
        comparison = True
    else:
        comparison = False

    context = {
        "cart": book_list,
        "total": total,
        "number": number,
        "comparison": comparison,
        "request": request,
    }
    return render(request, "cart_view.html", context)


# -----------------------------------------------------------------------------------------


def checkout(request):

    shipping_tokens = request.POST.get('shipng').split()
    number = cart_count(request)

    total = request.session.get('total')  # retrieves the total saved in the session

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
#  takes in a dictionary and creates a list of Book objects
#  also add up the total of the books in the list


def create_list(cart_items, book_id, quantity, request):
    # print(request.session.get(book_id))
    total = 0
    book_list = []  # holds the list of the books in the cart
    all_books = Book.objects.all()

    for book in cart_items:
        bk = all_books.get(title=book)
        book_price = float(bk.price)

        if book_id:
            if int(book_id) == int(bk.id):

                subtotal = round(book_price * float(quantity), 2)
                total = total + subtotal
                request.session[bk.title] = subtotal
                # print(request.session.get(int(bk.id)))
                request.session[bk.id] = quantity
                request.session.modified = True

            else:
                # print(str(bk.id) + " this is else")
                total = total + book_price
                request.session[bk.id] = 1

        else:
            total = total + book_price
            request.session[bk.title] = book_price
            request.session[bk.id] = 1

        request.session.modified = True
        book_list.append(bk)

    return round(total, 2), book_list


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

