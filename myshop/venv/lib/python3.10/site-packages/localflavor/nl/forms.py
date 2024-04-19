# -*- coding: utf-8 -*-
"""NL-specific validation helpers."""

from __future__ import unicode_literals

import six
from localflavor.exceptions import ValidationError
from localflavor.base import RegexValidator, Select
from localflavor.stub import _
from .nl_provinces import PROVINCE_CHOICES


class NLPostalCodeField(RegexValidator):
    """
    Validation for Dutch zip codes.

    .. versionadded:: 1.3
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format NNNN XX.')
    }

    def __init__(self):
        super(NLPostalCodeField, self).__init__(regex=r'^\d{4} ?[A-Z]{2}$')

    def clean(self, value):
        value = value.upper()
        value = super(NLPostalCodeField, self).clean(value)

        if int(value[:4]) < 1000:
            raise ValidationError(self.error_messages['invalid'])

        if isinstance(value, six.string_types):
            value = value.upper().replace(' ', '')

            if len(value) == 6:
                value = '%s %s' % (value[:4], value[4:])

        return super(NLPostalCodeField, self).clean(value)


class NLProvinceSelect(Select):
    """A Select widget that uses a list of provinces of the Netherlands as it's choices."""

    def __init__(self, attrs=None):
        super(NLProvinceSelect, self).__init__(attrs, choices=PROVINCE_CHOICES)
