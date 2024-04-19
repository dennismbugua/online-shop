# -*- coding: utf-8 -*-
"""Contains PT-specific Django form helpers."""


from __future__ import unicode_literals

from localflavor.base import RegexValidator, Select
from localflavor.stub import _

from .pt_regions import REGION_CHOICES

ZIP_CODE_REGEX = r'^[1-9]\d{3}-\d{3}$'


class PTRegionSelect(Select):
    """
    A select widget which uses a list of Portuguese regions as its choices.

    - Regions correspond to the Portuguese 'distritos' and 'regiões autónomas' as per ISO3166:2-PT.
    """

    def __init__(self, attrs=None):
        super(PTRegionSelect, self).__init__(attrs, choices=REGION_CHOICES)


class PTPostalCodeField(RegexValidator):
    """
    A field which validates Portuguese zip codes.

    NOTE
    - Postcode codes have the format XYYY-YYY (where X is a digit between 1 and 9 and Y is any other digit).
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XYYY-YYY'
                     ' (where X is a digit between 1 and 9 and Y is any other digit).'),
    }

    def __init__(self, *args, **kwargs):
        super(PTPostalCodeField, self).__init__(ZIP_CODE_REGEX, *args, **kwargs)
