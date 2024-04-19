"""AT-specific validation helpers."""
from __future__ import unicode_literals

import re

from localflavor.base import RegexValidator, Select
from localflavor.stub import _

from .at_states import STATE_CHOICES

re_ssn = re.compile(r'^\d{4} \d{6}')


class ATPostalCodeField(RegexValidator):
    """
    A form field that validates its input is an Austrian postcode.

    Accepts 4 digits (first digit must be greater than 0).
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXXX.'),
    }

    def __init__(self, *args, **kwargs):
        super(ATPostalCodeField, self).__init__(r'^[1-9]{1}\d{3}$', *args, **kwargs)


class ATStateSelect(Select):
    """A ``Select`` widget that uses a list of AT states as its choices."""

    def __init__(self, attrs=None):
        super(ATStateSelect, self).__init__(attrs, choices=STATE_CHOICES)
