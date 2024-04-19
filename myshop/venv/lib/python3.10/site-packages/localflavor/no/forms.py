"""Norwegian-specific validation helpers."""

from __future__ import unicode_literals

from localflavor.base import RegexValidator, Select
from localflavor.stub import _

from .no_municipalities import MUNICIPALITY_CHOICES


class NOPostalCodeField(RegexValidator):
    """
    A form field that validates input as a Norwegian zip code.

    Valid codes have four digits.
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXXX.'),
    }

    def __init__(self, *args, **kwargs):
        super(NOPostalCodeField, self).__init__(r'^\d{4}$', *args, **kwargs)


class NOMunicipalitySelect(Select):
    """A Select widget that uses a list of Norwegian municipalities (fylker) as its choices."""

    def __init__(self, attrs=None):
        super(NOMunicipalitySelect, self).__init__(attrs, choices=MUNICIPALITY_CHOICES)
