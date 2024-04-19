# -*- coding: utf-8 -*-
"""Mexican-specific form helpers."""
from __future__ import unicode_literals

from localflavor.base import RegexValidator, Select
from localflavor.stub import _

from .mx_states import STATE_CHOICES


class MXStateSelect(Select):
    """A Select widget that uses a list of Mexican states as its choices."""

    def __init__(self, attrs=None):
        super(MXStateSelect, self).__init__(attrs, choices=STATE_CHOICES)


class MXPostalCodeField(RegexValidator):
    """
    A form field that accepts a Mexican Postcode Code.

    More info about this:
        http://en.wikipedia.org/wiki/List_of_postal_codes_in_Mexico
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXXXX.'),
    }

    def __init__(self, *args, **kwargs):
        zip_code_re = r'^(0[1-9]|[1][0-6]|[2-9]\d)(\d{3})$'
        super(MXPostalCodeField, self).__init__(zip_code_re, *args, **kwargs)
