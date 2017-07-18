from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from books.models import Book
from datetime import *

# ----- Global Variables ---------------------------------------------

__not_modified = True   # used to determine if the cart as been modified
__grand_total = 0       # used to hold the current grand total of the cart
__shiping_code = '-T-'

# ----- Constants -----------------------------------------------------

REMOVE = -1  # identified for removing an item
DEFAULT = 1  # default quantity of a book

# ----- Function Views ------------------------------------------------


def add_cart(request, id):

    book = get_object_or_404(Book, id=id)

    quantity_holder = request.session.get('quantity', {})  # dict that will hold the book-id along with the quantities
    # of in the cart
    cart = request.session.get('cart', {})  # dict that will hold the book titles for the cart

    quantity_holder["book " + str(id)] = DEFAULT
    cart[id] = book.title
    request.session[book.title] = float(book.price)  # sets the 'subtotal' of the item to its price (default)

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

    cart_items = request.session.get('cart', {}).values()  # fetches the values stored in the session (Book titles)
    number = cart_count(request)

    total, book_list = create_list(cart_items, book_id, quantity, request)
    request.session['total'] = total

    # bottom code determines which button to display to the user. wont let checkout if total = 0
    comparison = get_comparison(total)

    context = {
        "cart": book_list,
        "total": total,
        "number": number,
        "comparison": comparison,
        "option": __shiping_code,
        "request": request
    }
    return render(request, "cart_view.html", context)


# -----------------------------------------------------------------------------------------


def view_cart(request):

    cart_items = request.session.get('cart', {}).values()  # fetches the values stored in the session

    number = cart_count(request)

    total, book_list = create_list(cart_items, None, DEFAULT, request)

    request.session['total'] = total

    comparison = get_comparison(total)

    context = {
        "cart": book_list,
        "total": total,
        "number": number,
        "comparison": comparison,
        "option": __shiping_code,
        "request": request,
    }
    return render(request, "cart_view.html", context)


# -----------------------------------------------------------------------------------------


def remove_item(request, id):

    cart = request.session.get('cart', {})
    quantity = request.session.get('quantity', {})

    del cart[id]
    del quantity["book " + id]

    request.session['cart'] = cart

    cart_items = cart.values()

    number = len(cart_items)

    total, book_list = create_list(cart_items, None, REMOVE, request)

    request.session['total'] = total

    comparison = get_comparison(total)

    context = {
        "cart": book_list,
        "total": total,
        "number": number,
        "comparison": comparison,
        "option": __shiping_code,
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

    global __not_modified
    global __grand_total

    total = 0
    book_list = []  # holds the list of the books in the cart
    all_books = Book.objects.all()
    holder = request.session.get('quantity', {})

    for book in cart_items:
        bk = all_books.get(title=book)
        book_price = float(bk.price)

        if book_id:

            __not_modified = False

            if int(book_id) == int(bk.id):

                subtotal = round(book_price * float(quantity), 2)
                total = total + subtotal
                request.session[bk.title] = subtotal  # this saves the 'title' along with the new subtotal in the session
                # in the dictionary

                holder["book " + str(book_id)] = quantity

                request.session.modified = True
            else:
                total = total + (book_price * float(holder["book " + str(bk.id)]))

        else:

            if __not_modified:

                total = total + book_price
                request.session[bk.title] = book_price

            else:

                if quantity == REMOVE:
                    total = 0
                    for books in cart_items:

                        bk = all_books.get(title=books)
                        book_price = float(bk.price)

                        total = total + (book_price * float(holder["book " + str(bk.id)]))

                else:
                    total = __grand_total

        book_list.append(bk)

    request.session['quantity'] = holder
    __grand_total = total  # updates the new total calculated to the global variable

    return round(total, 2), book_list


# -----------------------------------------------------------------------------------------
# --- Function bellow count the number of items in the dict 'cart'. this is used to display the number
# of items in the shopping cart all throughout the web application

def cart_count(request):
    cart = request.session.get('cart', {})
    cart_items = cart.values()  # fetches the values stored in the session

    number = len(cart_items)  # this is used to display the number of items in the cart

    return number


# -----------------------------------------------------------------------------------------
# ---Helper function below, reads in input from a radio option where it decodes and calculates the
# estimated delivery date along with the Shipping option


def decode_shipping(code):

    global __shiping_code
    dates = datetime.today()

    __shiping_code = code
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
# --- Helper function below accepts a var 'total'. This will help determine which button to display
# the user. If comparison is false, then the user wont be able to checkout


def get_comparison(total):

    if total > 0:
        comparison = True
    else:
        comparison = False

    return comparison

# -----------------------------------------------------------------------------------------
