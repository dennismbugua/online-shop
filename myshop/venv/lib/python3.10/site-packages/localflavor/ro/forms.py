# -*- coding: utf-8 -*-
"""Romanian specific form helpers."""
from __future__ import unicode_literals

from localflavor.stub import EMPTY_VALUES
from localflavor.base import CharValidator, RegexValidator, Select, ValidationError
from localflavor.stub import _

from .ro_counties import COUNTIES_CHOICES


class ROCountyField(CharValidator):
    """
    A form field that validates its input is a Romanian county name or abbreviation.

    It normalizes the input to the standard vehicle registration abbreviation for the given county.

    WARNING: This field will only accept names written with diacritics (using comma bellow for ș and ț); consider
    using ROCountySelect if this behavior is unacceptable for you

    For more information regarding diacritics see *Comma-below (ș and ț) versus cedilla (ş and ţ)* and
    *Unicode and HTML* sections from: `Romanian alphabet <https://en.wikipedia.org/wiki/Romanian_alphabet>`_.

    Example:
        | Argeș => valid (comma bellow)
        | Argeş => invalid (cedilla)
        | Arges => invalid (no diacritic)

    """

    default_error_messages = {
        'invalid': 'Enter a Romanian county code or name.',
    }

    def clean(self, value):
        super(ROCountyField, self).clean(value)

        if value in EMPTY_VALUES:
            return self.empty_value

        try:
            value = value.strip().upper()
        except AttributeError:
            pass

        # search for county code
        for entry in COUNTIES_CHOICES:
            if value in entry:
                return value

        # search for county name
        normalized_cc = []
        for entry in COUNTIES_CHOICES:
            normalized_cc.append((entry[0], entry[1].upper()))

        for entry in normalized_cc:
            if entry[1] == value:
                return entry[0]

        raise ValidationError(self.error_messages['invalid'])


class ROCountySelect(Select):
    """A Select widget that uses a list of Romanian counties (județe) as its choices."""

    def __init__(self, attrs=None):
        super(ROCountySelect, self).__init__(attrs, choices=COUNTIES_CHOICES)


class ROPostalCodeField(RegexValidator):
    """Romanian postal code field."""

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXXXXX.'),
    }

    def __init__(self, max_length=6, min_length=6, *args, **kwargs):
        super(ROPostalCodeField, self).__init__(
            r'^[0-9][0-8][0-9]{4}$', max_length=max_length,
            min_length=min_length, *args, **kwargs
        )
