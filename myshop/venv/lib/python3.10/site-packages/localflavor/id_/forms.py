"""ID-specific validation helpers."""

from __future__ import unicode_literals

import re

from localflavor.stub import EMPTY_VALUES
from localflavor.exceptions import ValidationError
from localflavor.base import CharValidator, Select
from localflavor.stub import _

postcode_re = re.compile(r'^[1-9]\d{4}$')


class IDPostalCodeField(CharValidator):
    """
    An Indonesian post code field.

    http://id.wikipedia.org/wiki/Kode_pos
    """

    default_error_messages = {
        'invalid': _('Enter a valid 5 digit postal code.'),
    }

    def clean(self, value):
        super(IDPostalCodeField, self).clean(value)
        if value in EMPTY_VALUES:
            return self.empty_value

        value = value.strip()
        if not postcode_re.search(value):
            raise ValidationError(self.error_messages['invalid'])

        if int(value) < 10110:
            raise ValidationError(self.error_messages['invalid'])

        # 1xxx0
        if value[0] == '1' and value[4] != '0':
            raise ValidationError(self.error_messages['invalid'])

        return '%s' % (value, )


class IDProvinceSelect(Select):
    """A Select widget that uses a list of provinces of Indonesia as its choices."""

    def __init__(self, attrs=None):
        # Load data in memory only when it is required, see also #17275
        from .id_choices import PROVINCE_CHOICES
        super(IDProvinceSelect, self).__init__(attrs, choices=PROVINCE_CHOICES)
