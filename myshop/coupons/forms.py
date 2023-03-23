# we need a way for customers to apply coupons to their purchases. The functionality to apply a coupon would be as follows:

# 1 The user adds products to the shopping cart.
# 2 The user can enter a coupon code in a form displayed in the shopping cart detail page.
# 3 When a user enters a coupon code and submits the form, we look for an existing coupon with the given code that is currently valid. We have to check that the coupon code matches the one entered by the user that the active attribute is True, and that the current datetime is between the valid_from and valid_to values.
# 4 If a coupon is found, we save it in the user's session and display the cart, including the discount applied to it and the updated total amount.
# 5 When the user places an order, we save the coupon to the given order.



from django import forms
from django.utils.translation import gettext_lazy as _

class CouponApplyForm(forms.Form):
    code = forms.CharField(label=_('Coupon'))
