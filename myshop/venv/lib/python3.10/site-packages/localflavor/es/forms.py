# -*- coding: utf-8 -*-
"""Spanish-specific validation helpers."""

from __future__ import unicode_literals

from localflavor.base import RegexValidator, Select
from localflavor.stub import _

from .es_provinces import PROVINCE_CHOICES
from .es_regions import REGION_CHOICES


class ESPostalCodeField(RegexValidator):
    """
    A form field that validates its input as a spanish postal code.

    Spanish postal code is a five digits string, with two first digits
    between 01 and 52, assigned to provinces code.
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the range and format 01XXX - 52XXX.'),
    }

    def __init__(self, *args, **kwargs):
        super(ESPostalCodeField, self).__init__(r'^(0[1-9]|[1-4][0-9]|5[0-2])\d{3}$', *args, **kwargs)


class ESRegionSelect(Select):
    """A Select widget that uses a list of spanish regions as its choices."""

    def __init__(self, attrs=None):
        super(ESRegionSelect, self).__init__(attrs, choices=REGION_CHOICES)


class ESProvinceSelect(Select):
    """A Select widget that uses a list of spanish provinces as its choices."""

    def __init__(self, attrs=None):
        super(ESProvinceSelect, self).__init__(attrs, choices=PROVINCE_CHOICES)
