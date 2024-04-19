from __future__ import unicode_literals

import re

from localflavor.exceptions import ValidationError
from localflavor.base import CharValidator, Select
from localflavor.stub import _, EMPTY_VALUES

from .lt_choices import COUNTY_CHOICES, MUNICIPALITY_CHOICES

postalcode = re.compile(r'^(LT\s?-\s?)?(?P<code>\d{5})$', re.IGNORECASE)


class LTCountySelect(Select):
    """A select field with the Lithuanian counties as choices."""

    def __init__(self, attrs=None):
        super(LTCountySelect, self).__init__(attrs, choices=COUNTY_CHOICES)


class LTMunicipalitySelect(Select):
    """A select field with the Lithuanian municipalities as choices."""

    def __init__(self, attrs=None):
        super(LTMunicipalitySelect, self).__init__(attrs,
                                                   choices=MUNICIPALITY_CHOICES)


class LTPostalCodeField(CharValidator):
    """
    A form field that validates and normalizes Lithanuan postal codes.

    Lithuanian postal codes in following forms accepted:
        * XXXXX
        * LT-XXXXX
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXXXX or LT-XXXXX.'),
    }

    def clean(self, value):
        value = super(LTPostalCodeField, self).clean(value)
        if value in EMPTY_VALUES:
            return self.empty_value

        match = re.match(postalcode, value)
        if not match:
            raise ValidationError(self.error_messages['invalid'])

        return 'LT-' + match.group('code')
