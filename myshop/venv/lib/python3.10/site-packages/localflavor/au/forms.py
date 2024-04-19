"""Australian-specific validation helpers."""

from __future__ import unicode_literals

from localflavor.base import RegexValidator, Select
from localflavor.stub import _

from .au_states import STATE_CHOICES


class AUPostalCodeField(RegexValidator):
    """
    Australian post code field.

    Assumed to be 4 digits.
    Northern Territory 3-digit postcodes should have leading zero.
    """

    default_error_messages = {
        'invalid': _('Enter a 4 digit postal code.'),
    }

    def __init__(self, max_length=4, *args, **kwargs):
        super(AUPostalCodeField, self).__init__(r'^\d{4}$', max_length=max_length, *args, **kwargs)


class AUStateSelect(Select):
    """A Select widget that uses a list of Australian states/territories as its choices."""

    def __init__(self, attrs=None):
        super(AUStateSelect, self).__init__(attrs, choices=STATE_CHOICES)
