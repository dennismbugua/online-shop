from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender


# In order to display the product catalog, we need to create a view
# to list all the products or filter products by a given category.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    # filter the QuerySet with available=True to retrieve only available products
    products = Product.objects.filter(available=True)
    if category_slug:
        # use an optional category_slug parameter to optionally filter products by a given category.
        language = request.LANGUAGE_CODE
        try:
            # Try to get category in current language
            category = get_object_or_404(Category,
                                         translations__language_code=language,
                                         translations__slug=category_slug)
        except:
            # If not found in current language, try with any available translation
            try:
                category = get_object_or_404(Category,
                                             translations__slug=category_slug)
            except:
                # If category doesn't exist, return all products
                category = None
        
        if category:
            products = products.filter(category=category)
    
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    # expects the id and slug parameters in order to retrieve the
    # Product instance. We can get this instance just through the ID
    # since it's a unique attribute. However, we include the slug in
    # the URL to build SEO-friendly URLs for products.
    language = request.LANGUAGE_CODE
    
    # Try to get product in current language first
    try:
        product = get_object_or_404(Product,
                                    id=id,
                                    translations__language_code=language,
                                    translations__slug=slug,
                                    available=True)
    except:
        # If not found in current language, try with any available translation
        try:
            product = get_object_or_404(Product,
                                        id=id,
                                        translations__slug=slug,
                                        available=True)
        except:
            # If still not found, try with just ID (fallback to default language)
            product = get_object_or_404(Product,
                                        id=id,
                                        available=True)
    
    cart_product_form = CartAddProductForm()

    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                  'cart_product_form': cart_product_form,
                  'recommended_products': recommended_products})
