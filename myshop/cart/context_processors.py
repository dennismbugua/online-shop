
# set the current cart into the request context. We will be able to access the cart in any template.
# Context processors can reside anywhere in your code, but creating them here will keep your code well organized

from .cart import Cart

def cart(request):
    return {'cart': Cart(request)}
