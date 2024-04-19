"""IT-specific validation helpers."""

from __future__ import unicode_literals

from localflavor.base import RegexValidator, Select
from localflavor.stub import _

from .it_provinces import PROVINCE_CHOICES
from .it_regions import REGION_CHOICES, REGION_PROVINCE_CHOICES


class ITPostalCodeField(RegexValidator):
    """
    A form field that validates input as an Italian zip code.

    Valid codes must have five digits.
    """

    default_error_messages = {
        'invalid': _('Enter a 5 digit ZIP code.'),
    }

    def __init__(self, *args, **kwargs):
        super(ITPostalCodeField, self).__init__(r'^\d{5}$', *args, **kwargs)


class ITRegionSelect(Select):
    """A Select widget that uses a list of IT regions as its choices."""

    def __init__(self, attrs=None):
        super(ITRegionSelect, self).__init__(attrs, choices=REGION_CHOICES)


class ITRegionProvinceSelect(Select):
    """A Select widget that uses a named group list of IT regions mapped to regions as its choices."""

    def __init__(self, attrs=None):
        super(ITRegionProvinceSelect, self).__init__(attrs, choices=REGION_PROVINCE_CHOICES)


class ITProvinceSelect(Select):
    """A Select widget that uses a list of IT provinces as its choices."""

    def __init__(self, attrs=None):
        super(ITProvinceSelect, self).__init__(attrs, choices=PROVINCE_CHOICES)
