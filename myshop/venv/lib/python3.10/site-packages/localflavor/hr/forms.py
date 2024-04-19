# -*- coding: utf-8 -*-
"""HR-specific validation helpers."""
from __future__ import unicode_literals

import re

from localflavor.stub import EMPTY_VALUES
from localflavor.exceptions import ValidationError
from localflavor.base import CharValidator, Select
from localflavor.stub import _

from .hr_counties import COUNTY_CHOICES

postal_code_re = re.compile(r'^\d{5}$')


class HRCountySelect(Select):
    """A Select widget that uses a list of counties of Croatia as its choices."""

    def __init__(self, attrs=None):
        super(HRCountySelect, self).__init__(attrs, choices=COUNTY_CHOICES)


class HRPostalCodeField(CharValidator):
    """
    Postal code of Croatia field.

    It consists of exactly five digits ranging from 10000 to possibly less than 60000.

    http://www.posta.hr/main.aspx?id=66
    """

    default_error_messages = {
        'invalid': _('Enter a valid 5 digit postal code.'),
    }

    def clean(self, value):
        super(HRPostalCodeField, self).clean(value)
        if value in EMPTY_VALUES:
            return self.empty_value

        value = value.strip()
        if not postal_code_re.search(value):
            raise ValidationError(self.error_messages['invalid'])

        # Make sure the number is in valid range.
        if not 9999 < int(value) < 60000:
            raise ValidationError(self.error_messages['invalid'])

        return '%s' % value
