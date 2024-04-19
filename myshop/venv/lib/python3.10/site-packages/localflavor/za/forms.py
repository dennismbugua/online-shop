"""South Africa-specific validation helpers."""
from __future__ import unicode_literals

from localflavor.base import RegexValidator, Select
from localflavor.stub import _


class ZAPostalCodeField(RegexValidator):
    """
    A form field that validates input as a South African postcode.

    Valid postcodes must have four digits.
    """

    default_error_messages = {
        'invalid': _('Enter a valid South African postal code in the format XXXX.'),
    }

    def __init__(self, *args, **kwargs):
        super(ZAPostalCodeField, self).__init__(r'^\d{4}$', *args, **kwargs)


class ZAProvinceSelect(Select):
    """A Select widget that uses a list of South African Provinces as its choices."""

    def __init__(self, attrs=None):
        from .za_provinces import PROVINCE_CHOICES
        super(ZAProvinceSelect, self).__init__(attrs, choices=PROVINCE_CHOICES)
