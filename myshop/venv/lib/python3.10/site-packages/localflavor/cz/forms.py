"""Czech-specific form helpers."""

from __future__ import unicode_literals

import re

from localflavor.base import RegexValidator, Select
from localflavor.stub import _

from .cz_regions import REGION_CHOICES

birth_number = re.compile(r'^(?P<birth>\d{6})/?(?P<id>\d{3,4})$')
ic_number = re.compile(r'^(?P<number>\d{7})(?P<check>\d)$')


class CZRegionSelect(Select):
    """A select widget widget with list of Czech regions as choices."""

    def __init__(self, attrs=None):
        super(CZRegionSelect, self).__init__(attrs, choices=REGION_CHOICES)


class CZPostalCodeField(RegexValidator):
    """
    A form field that validates its input as Czech postal code.

    Valid form is XXXXX or XXX XX, where X represents integer.
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXXXX or XXX XX.'),
    }

    def __init__(self, *args, **kwargs):
        super(CZPostalCodeField, self).__init__(r'^\d{5}$|^\d{3} \d{2}$', *args, **kwargs)

    def clean(self, value):
        """
        Validates the input and returns a string that contains only numbers.

        Returns an empty string for empty values.
        """
        value = super(CZPostalCodeField, self).clean(value)
        return value.replace(' ', '')
