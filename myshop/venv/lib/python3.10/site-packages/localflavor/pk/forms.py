"""Pakistani-specific validation helpers."""

from __future__ import unicode_literals

import re

from localflavor.base import RegexValidator, Select
from localflavor.stub import _

from .pk_states import STATE_CHOICES

POSTCODE_DIGITS_RE = re.compile(r'^(\d{5})$')


class PKPostalCodeField(RegexValidator):
    """
    Pakistani post code field.

    Assumed to be 5 digits.
    """

    default_error_messages = {
        'invalid': _('Enter a 5 digit postal code.'),
    }

    def __init__(self, *args, **kwargs):
        super(PKPostalCodeField, self).__init__(POSTCODE_DIGITS_RE, *args, **kwargs)


class PKStateSelect(Select):
    """A Select widget that uses a list of Pakistani states/territories as its choices."""

    def __init__(self, attrs=None):
        super(PKStateSelect, self).__init__(attrs, choices=STATE_CHOICES)
