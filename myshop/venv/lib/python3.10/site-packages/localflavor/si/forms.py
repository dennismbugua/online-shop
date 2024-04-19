"""Slovenian specific form helpers."""

from __future__ import unicode_literals

from localflavor.base import ChoiceField, Select
from localflavor.stub import _

from .si_postalcodes import SI_POSTALCODES_CHOICES


class SIPostalCodeField(ChoiceField):
    """Slovenian post codes field."""

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXXX.'),
    }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('choices', SI_POSTALCODES_CHOICES)
        super(SIPostalCodeField, self).__init__(*args, **kwargs)


class SIPostalCodeSelect(Select):
    """A Select widget that uses Slovenian postal codes as its choices."""

    def __init__(self, attrs=None):
        super(SIPostalCodeSelect, self).__init__(attrs,
                                                 choices=SI_POSTALCODES_CHOICES)
