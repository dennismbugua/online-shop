# -*- coding: utf-8 -*-
"""New Zealand specific form helpers."""
from __future__ import unicode_literals

from localflavor.base import RegexValidator, Select
from localflavor.stub import _

from .nz_provinces import PROVINCE_CHOICES
from .nz_regions import REGION_CHOICES


class NZRegionSelect(Select):
    """A select widget with list of New Zealand regions as its choices."""

    def __init__(self, attrs=None):
        super(NZRegionSelect, self).__init__(attrs, choices=REGION_CHOICES)


class NZProvinceSelect(Select):
    """A select widget with list of New Zealand provinces as its choices."""

    def __init__(self, attrs=None):
        super(NZProvinceSelect, self).__init__(attrs, choices=PROVINCE_CHOICES)


class NZPostalCodeField(RegexValidator):
    """A form field that validates its input as New Zealand postal code."""

    default_error_messages = {
        'invalid': _('Enter a 4 digit postal code.'),
    }

    def __init__(self, *args, **kwargs):
        super(NZPostalCodeField, self).__init__(r'^\d{4}$', *args, **kwargs)
