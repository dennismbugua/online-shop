from celery import shared_task
from django.core.mail import send_mail
from .models import Order


# We are going to create an asynchronous task to send an email notification to our users when they place an order. The convention is to include asynchronous tasks for your application in a tasks module within your application directory.

# Use asynchronous tasks not only for time-consuming processes, but also for other processes that are subject to failure, which do not take so much time to be executed, but which are subject to connection failures or require a retry policy.


@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is 
    successfully created.
    """
    order = Order.objects.get(id=order_id) # always recommended to pass only IDs to task functions and lookup objects when the task is executed
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order.\
                  Your order id is {}.'.format(order.first_name,
                                               order.id)
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [order.email])
    return mail_sent
