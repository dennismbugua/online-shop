import redis
from django.conf import settings
from .models import Product


# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


# allow us to store product purchases and retrieve product suggestions for a given product or products. The get_product_key() method receives an ID of a Product object and builds the Redis key for the sorted set where related products are stored, which looks like product:[id]:purchased_with.
class Recommender(object):

    def get_product_key(self, id):
        return 'product:{}:purchased_with'.format(id)

      
      
# method to store and score the products that were bought together
# The products_bought() method receives a list of Product objects that have been bought together (that is, belong to the same order). In this method, we perform the following tasks:
# 1 We get the product IDs for the given Product objects.
# 2 We iterate over the product IDs. For each ID, we iterate over the product IDs and skip the same product so that we get the products that are bought together with each product.
# 3 We get the Redis product key for each product bought using the get_product_id() method. For a product with an ID of 33, this method returns the key product:33:purchased_with. This is the key for the sorted set that contains the product IDs of products that were bought together with this one.
# 4 We increment the score of each product ID contained in the sorted set by 1. The score represents the times another product has been bought together with the given product.

    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # get the other products bought with each product
                if product_id != with_id:
                    # increment score for product purchased together
                    r.zincrby(self.get_product_key(product_id),
                              with_id,
                              amount=1)

                    
                    
                    
# The suggest_products_for() method receives the following parameters:

# products: This is a list of Product objects to get recommendations for. It can contain one or more products.
# max_results: This is an integer that represents the maximum number of recommendations to return.

# In this method, we perform the following actions:

# 1 We get the product IDs for the given Product objects.
# 2 If only one product is given, we retrieve the ID of the products that were bought together with the given product, ordered by the total number of times that they were bought together. To do so, we use Redis' ZRANGE command. We limit the number of results to the number specified in the max_results attribute (6 by default).
# 3 If more than one product is given, we generate a temporary Redis key built with the IDs of the products.
# 4 We combine and sum all scores for the items contained in the sorted set of each of the given products. This is done using the Redis' ZUNIONSTORE command. The ZUNIONSTORE command performs a union of the sorted sets with the given keys, and stores the aggregated sum of scores of the elements in a new Redis key. You can read more about this command at https://redis.io/commands/ZUNIONSTORE. We save the aggregated scores in the temporary key.
# 5 Since we are aggregating scores, we might obtain the same products we are getting recommendations for. We remove them from the generated sorted set using the ZREM command.
# 6 We retrieve the IDs of the products from the temporary key, ordered by their score using the ZRANGE command. We limit the number of results to the number specified in the max_results attribute. Then we remove the temporary key.
# 7 Finally, we get the Product objects with the given IDs and we order the products in the same order as them.

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # only 1 product
            suggestions = r.zrange(
                             self.get_product_key(product_ids[0]),
                             0, -1, desc=True)[:max_results]
        else:
            # generate a temporary key
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = 'tmp_{}'.format(flat_ids)
            # multiple products, combine scores of all products
            # store the resulting sorted set in a temporary key
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            # remove ids for the products the recommendation is for
            r.zrem(tmp_key, *product_ids)
            # get the product ids by their score, descendant sort
            suggestions = r.zrange(tmp_key, 0, -1, 
                                   desc=True)[:max_results]
            # remove the temporary key
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]

        # get suggested products and sort by order of appearance
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

      
    #  clear the recommendations
    def clear_purchases(self):
            for id in Product.objects.values_list('id', flat=True):
                r.delete(self.get_product_key(id))
