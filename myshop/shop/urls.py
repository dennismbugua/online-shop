from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # After building the product list and detail views, we have to define URL patterns for them
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, 
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),
]





# We have defined two different URL patterns for the product_list view: a pattern named
# product_list, which calls the product_list view without any parameters; and a pattern named
# product_list_by_category, which provides a category_slug parameter to the view for filtering
# products according to a given category. We added a pattern for the product_detail view, which
# passes the id and slug parameters to the view in order to retrieve a specific product.
