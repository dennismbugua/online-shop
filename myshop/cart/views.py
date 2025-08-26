from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm # include the coupon system in the cart's detail view
from shop.recommender import Recommender
import json


# adding products to the cart or updating quantities for existing products.
# We use the require_POST decorator to allow only POST requests, since this
# view is going to change data. The view receives the product ID as a parameter.
# We retrieve the Product instance with the given ID and validate CartAddProductForm.
# If the form is valid, we either add or update the product in the cart.
# The view redirects to the cart_detail URL that will display the content of the cart.



@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
        
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Return JSON response for AJAX requests
            response_data = {
                'success': True,
                'cart_total': float(cart.get_total_price()),
                'cart_total_after_discount': float(cart.get_total_price_after_discount()),
                'cart_items_count': len(cart),
                'message': 'Cart updated successfully'
            }
            return JsonResponse(response_data)
    else:
        # Handle form validation errors for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            response_data = {
                'success': False,
                'errors': form.errors,
                'message': 'Invalid form data'
            }
            return JsonResponse(response_data, status=400)
    
    return redirect('cart:cart_detail')


# remove items from the cart

# cart_remove view receives the product ID as a parameter. We retrieve the Product instance
# with the given ID and remove the product from the cart. Then, we redirect the user to the cart_detail URL.
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

# display the cart and its items
def cart_detail(request):
    cart = Cart(request)
    
    # allow users to change quantities from the cart detail page.
    for item in cart:
            item['update_quantity_form'] = CartAddProductForm(
                              initial={'quantity': item['quantity'],
                              'update': True})

    coupon_apply_form = CouponApplyForm()

    r = Recommender()
    cart_products = [item['product'] for item in cart]
    recommended_products = r.suggest_products_for(cart_products,
                                                  max_results=4)

    return render(request,
                  'cart/detail.html',
                  {'cart': cart,
                   'coupon_apply_form': coupon_apply_form,
                   'recommended_products': recommended_products})
