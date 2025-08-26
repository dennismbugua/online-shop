from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Order


# We are going to create an asynchronous task to send an email notification to our users when they place an order. The convention is to include asynchronous tasks for your application in a tasks module within your application directory.

# Use asynchronous tasks not only for time-consuming processes, but also for other processes that are subject to failure, which do not take so much time to be executed, but which are subject to connection failures or require a retry policy.


@shared_task
def order_created(order_id):
    """
    Task to send a stunning e-mail notification when an order is 
    successfully created.
    """
    order = Order.objects.get(id=order_id) # always recommended to pass only IDs to task functions and lookup objects when the task is executed
    
    subject = f'🎉 Order Received! Order #{order.id} - MyShop 🛍️'
    
    # Create HTML email content
    html_message = render_to_string('orders/order/email.html', {'order': order})
    
    # Create plain text content using template
    text_message = render_to_string('orders/order/email.txt', {'order': order})
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_message,
        from_email='🛍️ MyShop Team <noreply@myshop.com>',
        to=[order.email],
        reply_to=['💬 Support Team <support@myshop.com>']
    )
    
    # Attach HTML version
    email.attach_alternative(html_message, "text/html")
    
    mail_sent = email.send()
    return mail_sent
