"""FI-specific validation helpers."""

from __future__ import unicode_literals

from localflavor.base import RegexValidator, Select
from localflavor.stub import _

from .fi_municipalities import MUNICIPALITY_CHOICES


class FIPostalCodeField(RegexValidator):
    """
    A form field that validates input as a Finnish zip code.

    Valid codes consist of five digits.
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXXXX.'),
    }

    def __init__(self, *args, **kwargs):
        super(FIPostalCodeField, self).__init__(r'^\d{5}$', *args, **kwargs)


class FIMunicipalitySelect(Select):
    """A Select widget that uses a list of Finnish municipalities as its choices."""

    def __init__(self, attrs=None):
        super(FIMunicipalitySelect, self).__init__(attrs, choices=MUNICIPALITY_CHOICES)
