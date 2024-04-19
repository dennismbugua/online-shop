"""Israeli-specific form helpers."""
from __future__ import unicode_literals

from localflavor.base import RegexValidator
from localflavor.stub import _


class ILPostalCodeField(RegexValidator):
    """
    A form field that validates its input as an Israeli postal code.

    Valid form is XXXXX where X represents integer.
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXXXXXX or XXXXX, digits only.'),
    }

    def __init__(self, *args, **kwargs):
        super(ILPostalCodeField, self).__init__(r'^\d{5}$|^\d{7}$', *args, **kwargs)

    def clean(self, value):
        if value not in self.empty_values:
            value = value.replace(' ', '')
        return super(ILPostalCodeField, self).clean(value)
