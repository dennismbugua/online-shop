from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Coupon
from .forms import CouponApplyForm

@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['coupon_id'] = coupon.id
            messages.success(request, _('Coupon "{}" applied successfully! You saved {}% on your order.').format(code, coupon.discount))
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            # Check if coupon exists but is expired/inactive
            try:
                expired_coupon = Coupon.objects.get(code__iexact=code)
                if not expired_coupon.active:
                    messages.error(request, _('Coupon "{}" is no longer active. Please try a different coupon code.').format(code))
                elif expired_coupon.valid_to < now:
                    messages.error(request, _('Coupon "{}" has expired. Please check our current promotions for valid codes.').format(code))
                elif expired_coupon.valid_from > now:
                    messages.error(request, _('Coupon "{}" is not yet valid. Please check the promotion start date.').format(code))
                else:
                    messages.error(request, _('Coupon "{}" is not valid at this time.').format(code))
            except Coupon.DoesNotExist:
                messages.error(request, _('Coupon code "{}" does not exist. Please check the code and try again, or browse our current promotions.').format(code))
    else:
        messages.error(request, _('Please enter a valid coupon code.'))
    return redirect('cart:cart_detail')




# The coupon_apply view validates the coupon and stores it in the user's session. We apply the require_POST decorator to this view to restrict it to POST requests. In the view, we perform the following tasks:

# 1 We instantiate the CouponApplyForm form using the posted data and we check that the form is valid.
# 2 If the form is valid, we get the code entered by the user from the form's cleaned_data dictionary. We try to retrieve the Coupon object with the given code. We use the iexact field lookup to perform a case-insensitive exact match. The coupon has to be currently active (active=True) and valid for the current datetime. We use Django's timezone.now() function to get the current time zone-aware datetime and we compare it with the valid_from and valid_to fields performing lte (less than or equal to) and gte (greater than or equal to) field lookups, respectively.
# 3 We store the coupon ID in the user's session.
# 4 We redirect the user to the cart_detail URL to display the cart with the coupon applied.
