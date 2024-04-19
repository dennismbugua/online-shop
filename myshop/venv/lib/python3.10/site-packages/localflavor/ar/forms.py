# -*- coding: utf-8 -*-
"""AR-specific validation helpers."""

from __future__ import unicode_literals

from localflavor.exceptions import ValidationError
from localflavor.base import RegexValidator, Select
from localflavor.stub import _

from .ar_provinces import PROVINCE_CHOICES


class ARProvinceSelect(Select):
    """A Select widget that uses a list of Argentinean provinces/autonomous cities as its choices."""

    def __init__(self, attrs=None):
        super(ARProvinceSelect, self).__init__(attrs, choices=PROVINCE_CHOICES)


class ARPostalCodeField(RegexValidator):
    """
    Accepts a 'classic' NNNN Postal Code or a CPA.

    See:

    * http://www.correoargentino.com.ar/cpa/que_es
    * http://www.correoargentino.com.ar/cpa/como_escribirlo
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format NNNN or ANNNNAAA.'),
    }

    def __init__(self, max_length=8, min_length=4, *args, **kwargs):
        super(ARPostalCodeField, self).__init__(
            r'^\d{4}$|^[A-HJ-NP-Za-hj-np-z]\d{4}\D{3}$',
            max_length=max_length, min_length=min_length, *args, **kwargs
        )

    def clean(self, value):
        value = super(ARPostalCodeField, self).clean(value)
        if value in self.empty_values:
            return self.empty_value
        if len(value) not in (4, 8):
            raise ValidationError(self.error_messages['invalid'])
        if len(value) == 8:
            return '%s%s%s' % (value[0].upper(), value[1:5], value[5:].upper())
        return value
