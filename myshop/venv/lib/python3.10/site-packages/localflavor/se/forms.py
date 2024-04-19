# -*- coding: utf-8 -*-
"""Swedish specific validation helpers."""
from __future__ import unicode_literals

from localflavor.base import Select, RegexValidator
from localflavor.stub import _

from .se_counties import COUNTY_CHOICES

SE_POSTAL_CODE = r'^[1-9]\d{2} ?\d{2}$'


class SECountySelect(Select):
    """
    A Select form widget that uses a list of the Swedish counties (län) as its choices.

    The cleaned value is the official county code -- see
    http://en.wikipedia.org/wiki/Counties_of_Sweden for a list.
    """

    def __init__(self, attrs=None):
        super(SECountySelect, self).__init__(attrs=attrs,
                                             choices=COUNTY_CHOICES)


class SEPostalCodeField(RegexValidator):
    """
    A form field that validates input as a Swedish postal code (postnummer).

    Valid codes consist of five digits (XXXXX). The number can optionally be
    formatted with a space after the third digit (XXX XX).

    The cleaned value will never contain the space.
    """

    default_error_messages = {
        'invalid': _('Enter a Swedish postal code in the format XXXXX or XXX XX.'),
    }

    def __init__(self, *args, **kwargs):
        super(SEPostalCodeField, self).__init__(SE_POSTAL_CODE, *args, **kwargs)

    def clean(self, value):
        value = super(SEPostalCodeField, self).clean(value)
        if value in self.empty_values:
            return self.empty_value
        return value.replace(' ', '')
