"""Russian-specific forms helpers."""
from __future__ import unicode_literals

from localflavor.base import RegexValidator, Select
from localflavor.stub import _

from .ru_regions import RU_COUNTY_CHOICES, RU_REGIONS_CHOICES


class RUCountySelect(Select):
    """A Select widget that uses a list of Russian Counties as its choices."""

    def __init__(self, attrs=None):
        super(RUCountySelect, self).__init__(attrs, choices=RU_COUNTY_CHOICES)


class RURegionSelect(Select):
    """A Select widget that uses a list of Russian Regions as its choices."""

    def __init__(self, attrs=None):
        super(RURegionSelect, self).__init__(attrs, choices=RU_REGIONS_CHOICES)


class RUPostalCodeField(RegexValidator):
    """
    Russian Postal code field.

    Format: XXXXXX, where X is any digit, and first digit is not zero.
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXXXXX.'),
    }

    def __init__(self, *args, **kwargs):
        super(RUPostalCodeField, self).__init__(r'^\d{6}$', *args, **kwargs)
