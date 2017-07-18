from django import template

register = template.Library()


@register.filter
def get_subtotal(book, title):
    # this function gets the session from the template as 'book'
    # and gets the title passed from the template into 'title'

    # {{ request.session|get_subtotal:book.title }} <-- line 47 from cart_view.html
    # param 'book' = request.session and param 'title' = book.title

    subtotal = book.get(title)

    return subtotal


@register.filter
def update_quantity(book, id):

    holder = book.get('quantity', {})
    quantity = str(holder["book " + str(id)])

    return quantity
