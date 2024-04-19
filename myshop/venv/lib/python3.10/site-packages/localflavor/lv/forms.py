from __future__ import unicode_literals

import re

from localflavor.stub import EMPTY_VALUES
from localflavor.exceptions import ValidationError
from localflavor.base import CharValidator, Select
from localflavor.stub import _

from .lv_choices import MUNICIPALITY_CHOICES

zipcode = re.compile(r'^(LV\s?-\s?)?(?P<code>[1-5]\d{3})$', re.IGNORECASE)
idcode = re.compile(r'^(\d\d)(\d\d)(\d\d)-([0-2])(?:\d{3})(\d)$')


class LVPostalCodeField(CharValidator):
    """
    A form field that validates and normalizes Latvian postal codes.

    Latvian postal codes in following forms accepted:
        * XXXX
        * LV-XXXX
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXXX or LV-XXXX.'),
    }

    def clean(self, value):
        value = super(LVPostalCodeField, self).clean(value)
        if value in EMPTY_VALUES:
            return self.empty_value

        match = re.match(zipcode, value)
        if not match:
            raise ValidationError(self.error_messages['invalid'])

        return 'LV-' + match.group('code')


class LVMunicipalitySelect(Select):
    """A select field of Latvian municipalities."""

    def __init__(self, attrs=None):
        super(LVMunicipalitySelect, self).__init__(attrs, choices=MUNICIPALITY_CHOICES)
