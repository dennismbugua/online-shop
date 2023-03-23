from django.urls import reverse
from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint


def order_create(request):
    cart = Cart(request) # obtain the current cart from the session
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            # create an Order object using the save() method of the OrderCreateForm form. We avoid saving it to the database yet by using commit=False. If the cart contains a coupon, we store the related coupon and the discount that was applied. Then we save the order object to the database.
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            
            # launch asynchronous task
            # We call the delay() method of the task to execute it asynchronously. The task will be added to the queue and will be executed by a worker as soon as possible.
            order_created.delay(order.id)
            
            # after successfully creating an order, we set the order ID in the current session using the order_id session key. Then, we redirect the user to the payment:process URL
            # set the order in the session
            request.session['order_id'] = order.id
            
            # redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})

# Sometimes, you may want to customize the administration site beyond what is possible through configuring ModelAdmin, creating admin actions, and overriding admin templates. If this is the case, you need to create a custom admin view. With a custom view, you can build any functionality you need. You just have to make sure that only staff users can access your view and that you maintain the admin look and feel by making your template extend an admin template.
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})

# We use the staff_member_required decorator to make sure only staff users can access this view. We get the Order object with the given ID and we use the render_to_string() function provided by Django to render orders/order/pdf.html. The rendered HTML is saved in the html variable. Then, we generate a new HttpResponse object specifying the application/pdf content type and including the Content-Disposition header to specify the filename. We use WeasyPrint to generate a PDF file from the rendered HTML code and write the file to the HttpResponse object. We use the static file css/pdf.css to add CSS styles to the generated PDF file. We load it from the local path by using the STATIC_ROOT setting. Finally, we return the generated response.
@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + 'css/pdf.css')])
    return response
