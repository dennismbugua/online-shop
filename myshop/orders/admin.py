import csv
import datetime
from django.contrib import admin
from django.http import HttpResponse
from .models import Order, OrderItem
from django.urls import reverse
from django.utils.safestring import mark_safe


# Django escapes HTML output by default. We have to use the mark_safe function to avoid auto-escaping.
def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(
        reverse('orders:admin_order_detail', args=[obj.id])))



 # Sometimes, you might want to export the information contained in a model to a file so that you can import it in any other system. One of the most widely used formats to export/import data is Comma-Separated Values (CSV). A CSV file is a plain text file consisting of a number of records. There is usually one record per line, and some delimiter character, usually a literal comma, separates the record fields.

# In this code, we perform the following tasks:

# 1 We create an instance of HttpResponse, including a custom text/csv content type, to tell the browser that the response has to be treated as a CSV file. We also add a Content-Disposition header to indicate that the HTTP response contains an attached file.
# 2 We create a CSV writer object that will write on the response object.
# 3 We get the model fields dynamically using the get_fields() method of the model _meta options. We exclude many-to-many and one-to-many relationships.
# 4 We write a header row including the field names.
# 5 We iterate over the given QuerySet and write a row for each object returned by the QuerySet. We take care of formatting datetime objects because the output value for CSV has to be a string.
# 6 We customize the display name for the action in the template by setting a short_description attribute to the function.
    
def export_to_csv(modeladmin, request, queryset): 
    opts = modeladmin.model._meta 
    response = HttpResponse(content_type='text/csv') 
    response['Content-Disposition'] = 'attachment;' \
        'filename={}.csv'.format(opts.verbose_name) 
    writer = csv.writer(response) 
     
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many] 
    # Write a first row with header information 
    writer.writerow([field.verbose_name for field in fields]) 
    # Write data rows 
    for obj in queryset: 
        data_row = [] 
        for field in fields: 
            value = getattr(obj, field.name) 
            if isinstance(value, datetime.datetime): 
                value = value.strftime('%d/%m/%Y') 
            data_row.append(value) 
        writer.writerow(data_row) 
    return response 
export_to_csv.short_description = 'Export to CSV' 


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(
        reverse('orders:admin_order_pdf', args=[obj.id])))
order_pdf.short_description = 'Invoice'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated', order_detail, order_pdf]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
