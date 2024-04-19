"""DE-specific validation helpers."""

from __future__ import unicode_literals

from localflavor.base import RegexValidator, Select
from localflavor.stub import _

from .de_states import STATE_CHOICES


class DEPostalCodeField(RegexValidator):
    """A form field that validates input as a German zip code.

    Valid zip codes consist of five digits.
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXXXX.'),
    }

    def __init__(self, *args, **kwargs):
        super(DEPostalCodeField, self).__init__(r'^([0]{1}[1-9]{1}|[1-9]{1}[0-9]{1})[0-9]{3}$', *args, **kwargs)


class DEStateSelect(Select):
    """A Select widget that uses a list of DE states as its choices."""

    def __init__(self, attrs=None):
        super(DEStateSelect, self).__init__(attrs, choices=STATE_CHOICES)
