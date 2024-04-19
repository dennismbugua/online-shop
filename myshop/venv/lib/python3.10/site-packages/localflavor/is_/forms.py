"""Iceland specific form helpers."""

from __future__ import unicode_literals

from localflavor.base import CharValidator
from localflavor.stub import _

from .is_postalcodes import IS_POSTALCODES


class ISPostalCodeField(CharValidator):
    """Validates Icelandic postal codes as its choices."""

    default_error_messages = {
        'invalid': _('Enter a valid 3 digit postal code.'),
    }

    def __init__(self):
        super(ISPostalCodeField, self).__init__(
            min_length=None, max_length=None, choices=IS_POSTALCODES)
