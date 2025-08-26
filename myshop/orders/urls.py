from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _


app_name = 'orders'

urlpatterns = [
    path(_('create/'), views.order_create, name='order_create'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
    path('order/<int:order_id>/', views.order_created, name='order_created'),
    path('order/<int:order_id>/pdf/', views.order_pdf, name='order_pdf'),
    path('order/<int:order_id>/email-pdf/', views.email_order_pdf, name='email_order_pdf'),
    path('ajax/order/<int:order_id>/send-email/', views.ajax_send_email, name='ajax_send_email'),
]
