from __future__ import unicode_literals

from localflavor.exceptions import ValidationError
from localflavor.base import RegexValidator, Select
from localflavor.stub import _

from .tr_provinces import PROVINCE_CHOICES


class TRPostalCodeField(RegexValidator):
    """
    A form field that validates input as a Turkish zip code.

    Valid codes consist of five digits.
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXXXX.'),
    }

    def __init__(self, max_length=5, min_length=5, *args, **kwargs):
        super(TRPostalCodeField, self).__init__(
            r'^\d{5}$', max_length=max_length, min_length=min_length,
            *args, **kwargs
        )

    def clean(self, value):
        value = super(TRPostalCodeField, self).clean(value)
        if value in self.empty_values:
            return self.empty_value
        if len(value) != 5:
            raise ValidationError(self.error_messages['invalid'])
        province_code = int(value[:2])
        if province_code == 0 or province_code > 81:
            raise ValidationError(self.error_messages['invalid'])
        return value


class TRProvinceSelect(Select):
    """A Select widget that uses a list of provinces in Turkey as its choices."""

    def __init__(self, attrs=None):
        super(TRProvinceSelect, self).__init__(attrs, choices=PROVINCE_CHOICES)
