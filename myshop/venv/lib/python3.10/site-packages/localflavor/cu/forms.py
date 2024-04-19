# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from localflavor.exceptions import ValidationError
from localflavor.base import CharValidator, RegexValidator, Select
from localflavor.stub import _

from .choices import PROVINCE_CHOICES, PROVINCE_NORMALIZED, REGION_CHOICES, REGION_NORMALIZED


class CURegionField(CharValidator):
    """
    A form field for a Cuban region.

    The input is validated against a dictionary which includes names and abbreviations.
    It normalizes the input to the standard abbreviation for the given region.

    .. versionadded:: 1.6
    """

    default_error_messages = {
        'invalid': _('Enter a Cuban region.'),
    }
    description = _("Cuban regions (three uppercase letters)")

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = REGION_CHOICES
        kwargs['max_length'] = 3
        super(CURegionField, self).__init__(*args, **kwargs)

    def clean(self, value):
        super(CURegionField, self).clean(value)
        if value in self.empty_values:
            return self.empty_value
        try:
            return REGION_NORMALIZED[value.strip().lower()]
        except KeyError:
            pass
        raise ValidationError(self.error_messages['invalid'])


class CURegionSelect(Select):
    """
    A Select widget that uses a list of Cuban regions as its choices.

    .. versionadded:: 1.6
    """

    def __init__(self, attrs=None):
        super(CURegionSelect, self).__init__(attrs, choices=REGION_CHOICES)


class CUProvinceField(CharValidator):
    """
    A form field for a Cuban province.

    The input is validated against a dictionary which includes names and abbreviations.
    It normalizes the input to the standard abbreviation for the given province.

    .. versionadded:: 1.6
    """

    default_error_messages = {
        'invalid': _('Enter a Cuban province.'),
    }
    description = _("Cuban provinces (three uppercase letters)")

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = PROVINCE_CHOICES
        kwargs['max_length'] = 3
        super(CUProvinceField, self).__init__(*args, **kwargs)

    def clean(self, value):
        super(CUProvinceField, self).clean(value)
        if value in self.empty_values:
            return self.empty_value
        try:
            return PROVINCE_NORMALIZED[value.strip().lower()]
        except KeyError:
            pass
        raise ValidationError(self.error_messages['invalid'])


class CUProvinceSelect(Select):
    """
    A Select widget that uses a list of Cuban provinces as its choices.

    .. versionadded:: 1.6
    """

    def __init__(self, attrs=None):
        super(CUProvinceSelect, self).__init__(attrs, choices=PROVINCE_CHOICES)


class CUPostalCodeField(RegexValidator):
    """
    A form field for a Cuban postal Code.

    Taken from : http://mapanet.eu/Postal_Codes/?C=CU

    The Cuban postal code is a combination of 5 digits non begin with 0.

    .. versionadded:: 1.6
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXXXX.'),
    }
    description = _("Cuban postal code")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 5
        super(CUPostalCodeField, self).__init__(r'^[1-9]\d{4}$', *args, **kwargs)
