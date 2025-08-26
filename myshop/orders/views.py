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
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import weasyprint
import os


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
            
            # launch asynchronous task or send email synchronously in development
            try:
                # Try to launch asynchronous task
                order_created.delay(order.id)
            except Exception as e:
                # If Celery is not running, send email synchronously with beautiful template
                try:
                    from django.core.mail import EmailMultiAlternatives
                    from django.template.loader import render_to_string
                    
                    subject = f'🎉 Order Confirmation #{order.id} - MyShop'
                    
                    # Create HTML email content using beautiful template
                    html_message = render_to_string('orders/order/email.html', {'order': order})
                    
                    # Create plain text content using beautiful template
                    text_message = render_to_string('orders/order/email.txt', {'order': order})
                    
                    email = EmailMultiAlternatives(
                        subject=subject,
                        body=text_message,
                        from_email='🛍️ MyShop Team <noreply@myshop.com>',
                        to=[order.email],
                        reply_to=['support@myshop.com']
                    )
                    
                    # Attach HTML version
                    email.attach_alternative(html_message, "text/html")
                    
                    email.send()
                except Exception:
                    # If email fails, continue anyway
                    pass
            
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


# Public order PDF view (for customers)
def order_created(request, order_id):
    """Display order created/success page"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order/created.html', {'order': order})


def order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + 'css/pdf.css')])
    return response


# Email order PDF view
def email_order_pdf(request, order_id):
    from django.http import JsonResponse
    from django.core.mail import send_mail
    import logging
    
    logger = logging.getLogger(__name__)
    
    # Debug: Log the request method
    logger.info(f"Request method: {request.method}")
    logger.info(f"Order ID: {order_id}")
    
    if request.method == 'POST':
        try:
            order = get_object_or_404(Order, id=order_id)
            logger.info(f"Processing email request for order {order.id}")
            
            # Simplified email sending for testing
            subject = f'🎉 Order Confirmation #{order.id} - MyShop'
            message = f"""
Hello {order.first_name} {order.last_name},

Thank you for your order! Your order #{order.id} has been confirmed.

Order Total: ${order.get_total_cost()}

We'll send you an update when your order ships.

Best regards,
MyShop Team
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    'MyShop <noreply@myshop.com>',
                    [order.email],
                    fail_silently=False,
                )
                logger.info(f"Email sent successfully to {order.email}")
                
                return JsonResponse({
                    'success': True, 
                    'message': 'Email sent successfully! Check your inbox.'
                })
            except Exception as email_error:
                logger.error(f"Error sending email: {str(email_error)}")
                return JsonResponse({
                    'success': False, 
                    'message': f'Failed to send email: {str(email_error)}'
                })
            
        except Exception as e:
            logger.error(f"Error in email view: {str(e)}")
            return JsonResponse({
                'success': False, 
                'message': f'Server error: {str(e)}'
            })
    else:
        # For GET requests, just download a simple PDF
        try:
            order = get_object_or_404(Order, id=order_id)
            
            # Simple PDF content
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Order {order.id} Receipt</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ text-align: center; margin-bottom: 30px; }}
                    .order-info {{ margin-bottom: 20px; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>MyShop Order Receipt</h1>
                    <p>Order #{order.id}</p>
                </div>
                <div class="order-info">
                    <p><strong>Customer:</strong> {order.first_name} {order.last_name}</p>
                    <p><strong>Email:</strong> {order.email}</p>
                    <p><strong>Total:</strong> ${order.get_total_cost()}</p>
                    <p><strong>Date:</strong> {order.created}</p>
                </div>
            </body>
            </html>
            """
            
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename=MyShop_Order_{order.id}_Receipt.pdf'
            
            # Simple PDF generation without external CSS
            weasyprint.HTML(string=html_content).write_pdf(response)
            return response
            
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            return JsonResponse({
                'success': False, 
                'message': f'Failed to generate PDF: {str(e)}'
            })


def ajax_send_email(request, order_id):
    """
    Dedicated AJAX endpoint for sending email PDF receipts
    """
    from django.http import JsonResponse
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string
    from io import BytesIO
    import weasyprint
    import logging
    
    logger = logging.getLogger(__name__)
    logger.info(f"AJAX request received: Method={request.method}, Order ID={order_id}")
    
    # Check if it's a POST request
    if request.method != 'POST':
        return JsonResponse({
            'success': False, 
            'message': f'Method {request.method} not allowed. Please use POST.'
        }, status=405)
    
    try:
        order = get_object_or_404(Order, id=order_id)
        logger.info(f"Processing AJAX email request for order {order.id}")
        
        # Create beautiful email with HTML template
        subject = f'🎉 Your Amazing Order #{order.id} is Confirmed! - MyShop ✨'
        
        # Create HTML email content
        try:
            html_message = render_to_string('orders/order/email.html', {'order': order})
            logger.info("HTML email template rendered successfully")
        except Exception as e:
            logger.error(f"Error rendering HTML template: {str(e)}")
            # Fallback to beautiful HTML
            html_message = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Order Confirmation - MyShop</title>
                <style>
                    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                    body {{ 
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                        line-height: 1.6; color: #333; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; 
                    }}
                    .email-container {{ 
                        max-width: 600px; margin: 0 auto; background: #ffffff; 
                        border-radius: 20px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15); 
                        overflow: hidden; position: relative; 
                    }}
                    .email-container::before {{ 
                        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 6px; 
                        background: linear-gradient(90deg, #10b981, #059669, #6366f1, #8b5cf6); 
                    }}
                    .header {{ 
                        background: linear-gradient(135deg, #10b981, #059669); 
                        color: white; padding: 40px 30px; text-align: center; 
                    }}
                    .header h1 {{ 
                        font-size: 2.5rem; font-weight: 800; margin: 0 0 10px 0; 
                        text-shadow: 0 2px 4px rgba(0,0,0,0.1); 
                    }}
                    .header p {{ 
                        font-size: 1.2rem; margin: 0; opacity: 0.9; 
                    }}
                    .content {{ padding: 40px 30px; }}
                    .greeting {{ 
                        text-align: center; margin-bottom: 30px; 
                    }}
                    .greeting h2 {{ 
                        color: #1f2937; margin: 0 0 10px 0; font-size: 1.8rem; 
                    }}
                    .greeting p {{ 
                        color: #6b7280; font-size: 1.1rem; margin: 0; 
                    }}
                    .order-box {{ 
                        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.05)); 
                        border: 2px solid rgba(16, 185, 129, 0.3); 
                        border-radius: 15px; padding: 25px; margin: 30px 0; 
                        position: relative; overflow: hidden; 
                    }}
                    .order-box::before {{ 
                        content: ''; position: absolute; top: -50%; left: -50%; 
                        width: 200%; height: 200%; 
                        background: linear-gradient(45deg, transparent, rgba(16, 185, 129, 0.1), transparent); 
                        animation: shimmer 3s ease-in-out infinite; 
                    }}
                    @keyframes shimmer {{ 
                        0%, 100% {{ transform: translateX(-100%) translateY(-100%); }} 
                        50% {{ transform: translateX(100%) translateY(100%); }} 
                    }}
                    .order-box h3 {{ 
                        color: #059669; margin: 0 0 20px 0; text-align: center; 
                        font-size: 1.4rem; position: relative; z-index: 1; 
                    }}
                    .order-row {{ 
                        display: flex; justify-content: space-between; align-items: center; 
                        margin-bottom: 12px; padding: 8px 0; border-bottom: 1px solid rgba(16, 185, 129, 0.1); 
                        position: relative; z-index: 1; 
                    }}
                    .order-row:last-child {{ border-bottom: none; }}
                    .order-row .label {{ font-weight: 600; }}
                    .order-row .value {{ color: #059669; font-weight: 700; }}
                    .order-row .total {{ font-size: 1.3rem; color: #059669; }}
                    .next-steps {{ 
                        background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.2); 
                        border-radius: 15px; padding: 25px; margin: 30px 0; 
                    }}
                    .next-steps h3 {{ 
                        color: #4338ca; margin: 0 0 15px 0; text-align: center; 
                    }}
                    .next-steps ul {{ 
                        margin: 0; padding-left: 20px; color: #374151; 
                    }}
                    .next-steps li {{ 
                        margin-bottom: 8px; 
                    }}
                    .cta-section {{ 
                        text-align: center; margin: 40px 0; 
                    }}
                    .cta-button {{ 
                        background: linear-gradient(135deg, #6366f1, #8b5cf6); 
                        color: white; padding: 15px 30px; border-radius: 25px; 
                        text-decoration: none; font-weight: 600; display: inline-block; 
                        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3); 
                        transition: transform 0.3s ease; 
                    }}
                    .cta-button:hover {{ 
                        transform: translateY(-2px); 
                        box-shadow: 0 12px 36px rgba(99, 102, 241, 0.4); 
                    }}
                    .footer {{ 
                        background: #f8fafc; padding: 25px 30px; text-align: center; 
                        border-top: 1px solid #e5e7eb; 
                    }}
                    .footer p {{ 
                        margin: 0; color: #6b7280; font-size: 0.9rem; 
                    }}
                    .footer a {{ 
                        color: #6366f1; text-decoration: none; font-weight: 600; 
                    }}
                    .social-links {{ 
                        margin-top: 15px; 
                    }}
                    .social-links a {{ 
                        display: inline-block; margin: 0 10px; color: #6b7280; 
                        font-size: 1.2rem; text-decoration: none; 
                    }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="header">
                        <h1>🎉 Order Confirmed!</h1>
                        <p>Thank you for shopping with MyShop</p>
                    </div>
                    
                    <div class="content">
                        <div class="greeting">
                            <h2>Hello {order.first_name} {order.last_name}! ✨</h2>
                            <p>Your order has been successfully placed and is being processed with care.</p>
                        </div>
                        
                        <div class="order-box">
                            <h3>📦 Order Summary</h3>
                            <div class="order-row">
                                <span class="label">Order Number:</span>
                                <span class="value">#{order.id}</span>
                            </div>
                            <div class="order-row">
                                <span class="label">Order Date:</span>
                                <span class="value">{order.created.strftime('%B %d, %Y')}</span>
                            </div>
                            <div class="order-row">
                                <span class="label">Payment Status:</span>
                                <span class="value">✅ Confirmed</span>
                            </div>
                            <div class="order-row">
                                <span class="label">Shipping Address:</span>
                                <span class="value">{order.address}, {order.city} {order.postal_code}</span>
                            </div>
                            <div class="order-row">
                                <span class="label total">Total Amount:</span>
                                <span class="value total">${order.get_total_cost()}</span>
                            </div>
                        </div>
                        
                        <div class="next-steps">
                            <h3>🚀 What Happens Next?</h3>
                            <ul>
                                <li>✨ Your order is being carefully prepared by our amazing team</li>
                                <li>✨ You'll receive shipping confirmation within 24-48 hours</li>
                                <li>✨ Track your package in real-time with the tracking number we'll provide</li>
                                <li>✨ Enjoy fast and secure delivery right to your doorstep</li>
                            </ul>
                        </div>
                        
                        <div class="cta-section">
                            <p style="color: #6b7280; margin-bottom: 20px;">Ready for more amazing products?</p>
                            <a href="#" class="cta-button">🛒 Continue Shopping</a>
                        </div>
                        
                        <div style="text-align: center; color: #6b7280; margin-top: 30px;">
                            <p>Thank you for choosing MyShop! We truly appreciate your business and trust.</p>
                        </div>
                    </div>
                    
                    <div class="footer">
                        <p>Questions? We're here to help! Contact us at <a href="mailto:support@myshop.com">support@myshop.com</a></p>
                        <div class="social-links">
                            <a href="#">📘</a>
                            <a href="#">📷</a>
                            <a href="#">🐦</a>
                        </div>
                        <p style="margin-top: 15px; font-size: 0.8rem;">
                            © 2025 MyShop. All rights reserved. | Made with ❤️ for our customers
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
        
        # Create plain text content
        try:
            text_message = render_to_string('orders/order/email.txt', {'order': order})
            logger.info("Text email template rendered successfully")
        except Exception as e:
            logger.error(f"Error rendering text template: {str(e)}")
            # Fallback to beautiful text
            text_message = f"""
🎉✨ ORDER CONFIRMATION - MyShop ✨🎉

Hello {order.first_name} {order.last_name}!

Congratulations! Your order has been successfully confirmed! 🎊

╔══════════════════════════════════════════════════════════════╗
║                        📦 ORDER SUMMARY                       ║
╚══════════════════════════════════════════════════════════════╝

🔢 Order Number: #{order.id}
📅 Order Date: {order.created.strftime('%B %d, %Y')}
✅ Payment Status: CONFIRMED & SECURED
💰 Total Amount: ${order.get_total_cost()}

📍 SHIPPING ADDRESS:
   {order.address}
   {order.city}, {order.postal_code}

╔══════════════════════════════════════════════════════════════╗
║                    🚀 WHAT HAPPENS NEXT?                     ║
╚══════════════════════════════════════════════════════════════╝

✨ Your order is being carefully prepared by our amazing team
✨ You'll receive shipping confirmation within 24-48 hours  
✨ Track your package in real-time with our tracking system
✨ Enjoy fast and secure delivery right to your doorstep
✨ We'll keep you updated every step of the way!

╔══════════════════════════════════════════════════════════════╗
║                      💝 THANK YOU!                           ║
╚══════════════════════════════════════════════════════════════╝

We're absolutely thrilled to have you as our valued customer! 
Your support means the world to us, and we can't wait for you 
to receive your amazing order.

🎯 NEED HELP? We're here for you!
   📧 Email: support@myshop.com
   🌐 Website: www.myshop.com
   📱 Phone: 1-800-MYSHOP

🛒 Ready for more? Check out our latest arrivals and exclusive deals!

Happy Shopping! 🎉✨

With love and appreciation,
The MyShop Team ❤️

─────────────────────────────────────────────────────────────
© 2025 MyShop. All rights reserved. | Made with ❤️ for our customers
            """
        
        # Create email message
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email='MyShop Team 🛒 <mcdennislonell@gmail.com>',
            to=[order.email],
            reply_to=['support@myshop.com']
        )
        
        # Attach HTML version
        email.attach_alternative(html_message, "text/html")
        logger.info("Email message created successfully")

        # Generate and attach PDF receipt
        try:
            # Create PDF content
            try:
                pdf_html = render_to_string('orders/order/pdf.html', {'order': order})
            except Exception:
                # Fallback PDF content
                pdf_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>Order {order.id} Receipt</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 20px; }}
                        .header {{ text-align: center; margin-bottom: 30px; border-bottom: 2px solid #ccc; padding-bottom: 20px; }}
                        .order-info {{ margin-bottom: 20px; }}
                        .customer-info {{ background: #f9f9f9; padding: 15px; border-radius: 5px; }}
                        .total {{ font-size: 1.2em; font-weight: bold; color: #059669; text-align: right; margin-top: 20px; }}
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>MyShop Receipt</h1>
                        <h2>Order #{order.id}</h2>
                        <p>Date: {order.created.strftime('%B %d, %Y')}</p>
                    </div>
                    
                    <div class="customer-info">
                        <h3>Customer Information</h3>
                        <p><strong>Name:</strong> {order.first_name} {order.last_name}</p>
                        <p><strong>Email:</strong> {order.email}</p>
                        <p><strong>Address:</strong><br>
                           {order.address}<br>
                           {order.city}, {order.postal_code}</p>
                    </div>
                    
                    <div class="total">
                        <p>Total Amount: ${order.get_total_cost()}</p>
                    </div>
                    
                    <div style="margin-top: 30px; text-align: center; font-size: 0.9em; color: #666;">
                        <p>Thank you for your business!</p>
                        <p>MyShop - Your trusted online store</p>
                    </div>
                </body>
                </html>
                """
            
            # Generate PDF
            out = BytesIO()
            # Use simple inline CSS since external CSS might not be available
            css = weasyprint.CSS(string="""
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { text-align: center; margin-bottom: 30px; border-bottom: 2px solid #ccc; padding-bottom: 20px; }
                .order-info { margin-bottom: 20px; }
                .customer-info { background: #f9f9f9; padding: 15px; border-radius: 5px; }
                .total { font-size: 1.2em; font-weight: bold; color: #059669; text-align: right; margin-top: 20px; }
            """)
            
            weasyprint.HTML(string=pdf_html).write_pdf(out, stylesheets=[css])
            logger.info("PDF generated successfully")
            
            # Attach PDF file
            email.attach(f'MyShop_Order_{order.id}_Receipt.pdf',
                         out.getvalue(),
                         'application/pdf')
            logger.info("PDF attached to email successfully")
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            # Continue without PDF attachment - still send the email
        
        # Send email
        try:
            email.send()
            logger.info(f"Email sent successfully to {order.email}")
            
            return JsonResponse({
                'success': True, 
                'message': f'🎉 Confirmation email receipt sent to <strong>{order.email}</strong>! <br/> ✨ Check your inbox for order details!'
            })
        except Exception as email_error:
            logger.error(f"Error sending email: {str(email_error)}")
            return JsonResponse({
                'success': False, 
                'message': f'Failed to send email: {str(email_error)}. Please check your email settings.'
            })
        
    except Exception as e:
        logger.error(f"Error in AJAX email view: {str(e)}")
        return JsonResponse({
            'success': False, 
            'message': f'Server error: {str(e)}'
        })
