"""Greek-specific forms helpers."""

from localflavor.base import RegexValidator
from localflavor.stub import _


class GRPostalCodeField(RegexValidator):
    """
    Greek Postal code field.

    Format: XXXXX, where X is any digit, and first digit is not 0 or 9.
    """

    default_error_messages = {
        'invalid': _('Enter a valid 5-digit postal code.'),
    }

    def __init__(self, *args, **kwargs):
        super(GRPostalCodeField, self).__init__(r'^[12345678]\d{4}$', *args, **kwargs)
