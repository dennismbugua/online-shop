"""Singapore-specific validation helpers."""

from __future__ import unicode_literals

from localflavor.base import RegexValidator
from localflavor.stub import _


class SGPostalCodeField(RegexValidator):
    """
    Singapore post code field.

    Assumed to be 6 digits.
    """

    default_error_messages = {
        'invalid': _('Enter a 6-digit postal code.'),
    }

    def __init__(self, *args, **kwargs):
        super(SGPostalCodeField, self).__init__(r'^\d{6}$', *args, **kwargs)
