from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    translations = TranslatedFields(
            name = models.CharField(max_length=200,
                                    db_index=True),
            slug = models.SlugField(max_length=200,
                                    db_index=True,
                                    unique=True)
        )

    class Meta:
        # ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self): # the convention to retrieve the URL for a given object
            return reverse('shop:product_list_by_category',
                           args=[self.slug])


class Product(TranslatableModel):
    translations = TranslatedFields(
            name = models.CharField(max_length=200, db_index=True),
            slug = models.SlugField(max_length=200, db_index=True),
            description = models.TextField(blank=True)
        )
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    # For the price field, we use DecimalField instead of FloatField to avoid rounding issues.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
# use the index_together meta option to specify
# an index for the id and slug fields together.
# We define this index because we plan to query
# products by both id and slug. Both fields are indexed
# together to improve performances for queries that utilize
# the two fields.
    
    
    

    #class Meta:
    #    ordering = ('name',)
    #    index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self): # the convention to retrieve the URL for a given object
            return reverse('shop:product_detail',
                           args=[self.id, self.slug])
