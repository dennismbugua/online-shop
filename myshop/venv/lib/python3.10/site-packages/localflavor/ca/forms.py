"""Canada-specific validation helpers."""

from __future__ import unicode_literals

import re

from localflavor.stub import EMPTY_VALUES
from localflavor.exceptions import ValidationError
from localflavor.base import CharValidator, Select
from localflavor.stub import _


class CAPostalCodeField(CharValidator):
    """
    Canadian postal code form field.

    Validates against known invalid characters: D, F, I, O, Q, U
    Additionally the first character cannot be Z or W.
    For more info see:
    http://www.canadapost.ca/tools/pg/manual/PGaddress-e.asp#1402170
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXX XXX.'),
    }

    postcode_regex = re.compile(
        r'^([ABCEGHJKLMNPRSTVXY]\d[ABCEGHJKLMNPRSTVWXYZ]) *(\d[ABCEGHJKLMNPRSTVWXYZ]\d)$')

    def clean(self, value):
        value = super(CAPostalCodeField, self).clean(value)
        postcode = value.upper().strip()
        m = self.postcode_regex.match(postcode)
        if not m:
            raise ValidationError(self.error_messages['invalid'])
        return "%s %s" % (m.group(1), m.group(2))


class CAProvinceField(CharValidator):
    """
    A form field that validates its input is a Canadian province name or abbreviation.

    It normalizes the input to the standard two-leter postal service
    abbreviation for the given province.
    """

    default_error_messages = {
        'invalid': _('Enter a Canadian province or territory.'),
    }

    def clean(self, value):
        super(CAProvinceField, self).clean(value)
        if value in EMPTY_VALUES:
            return self.empty_value
        try:
            value = value.strip().lower()
        except AttributeError:
            pass
        else:
            # Load data in memory only when it is required, see also #17275
            from .ca_provinces import PROVINCES_NORMALIZED
            try:
                return PROVINCES_NORMALIZED[value.strip().lower()]
            except KeyError:
                pass
        raise ValidationError(self.error_messages['invalid'])


class CAProvinceSelect(Select):
    """A Select widget that uses a list of Canadian provinces and territories as its choices."""

    def __init__(self, attrs=None):
        # Load data in memory only when it is required, see also #17275
        from .ca_provinces import PROVINCE_CHOICES
        super(CAProvinceSelect, self).__init__(attrs, choices=PROVINCE_CHOICES)
