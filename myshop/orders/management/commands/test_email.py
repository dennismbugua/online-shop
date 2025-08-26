from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from orders.models import Order


class Command(BaseCommand):
    help = 'Test the enhanced email templates'

    def add_arguments(self, parser):
        parser.add_argument('--order-id', type=int, help='Order ID to test email with')

    def handle(self, *args, **options):
        order_id = options.get('order_id')
        
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Order with ID {order_id} does not exist')
                )
                return
        else:
            # Get the latest order
            order = Order.objects.filter().first()
            if not order:
                self.stdout.write(
                    self.style.ERROR('No orders found. Create an order first.')
                )
                return

        self.stdout.write(
            self.style.SUCCESS(f'Testing email for Order #{order.id}')
        )

        # Create email content
        subject = f'🎉 Order Confirmation #{order.id} - MyShop'
        
        # Create HTML email content
        html_message = render_to_string('orders/order/email.html', {'order': order})
        
        # Create plain text content using template
        text_message = render_to_string('orders/order/email.txt', {'order': order})
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email='MyShop <noreply@myshop.com>',
            to=[order.email],
            reply_to=['support@myshop.com']
        )
        
        # Attach HTML version
        email.attach_alternative(html_message, "text/html")
        
        try:
            email.send()
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Email sent successfully to {order.email}!\n'
                    f'Check your terminal console for the email content.'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to send email: {str(e)}')
            )
