from django.contrib import admin
from .models import Category, Product
from parler.admin import TranslatableAdmin


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']

    def get_prepopulated_fields(self, request, obj=None):
            return {'slug': ('name',)}
        
# use the prepopulated_fields attribute to specify fields where
# the value is automatically set using the value of other fields.
# As you have seen before, this is convenient for generating slugs.



@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']

    def get_prepopulated_fields(self, request, obj=None):
            return {'slug': ('name',)}

        
# use the list_editable attribute in the ProductAdmin class to
# set the fields that can be edited from the list display page
# of the administration site. This will allow you to edit
# multiple rows at once. Any field in list_editable must also be
# listed in the list_display attribute since only the fields
# displayed can be edited.
