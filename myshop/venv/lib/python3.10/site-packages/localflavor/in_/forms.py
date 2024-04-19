"""India-specific validation helpers."""

from __future__ import unicode_literals

import re

from localflavor.stub import EMPTY_VALUES
from localflavor.exceptions import ValidationError
from localflavor.base import CharValidator, RegexValidator, Select
from localflavor.stub import _

from .in_states import STATE_CHOICES, STATES_NORMALIZED


class INPostalCodeField(RegexValidator):
    """A form field that validates input as an Indian zip code, with the format XXXXXXX."""

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXXXXX or XXX XXX.'),
    }

    def __init__(self, *args, **kwargs):
        super(INPostalCodeField, self).__init__(r'^\d{3}\s?\d{3}$', *args, **kwargs)

    def clean(self, value):
        value = super(INPostalCodeField, self).clean(value)
        if value in self.empty_values:
            return self.empty_value
        # Convert to "NNNNNN" if "NNN NNN" given
        value = re.sub(r'^(\d{3})\s(\d{3})$', r'\1\2', value)
        return value


class INStateField(CharValidator):
    """
    A form field that validates its input is a Indian state name or abbreviation.

    It normalizes the input to the standard two-letter vehicle
    registration abbreviation for the given state or union territory

    .. versionchanged:: 1.1

       Added Telangana to list of states. More details at
       https://en.wikipedia.org/wiki/Telangana#Bifurcation_of_Andhra_Pradesh

    """

    default_error_messages = {
        'invalid': _('Enter an Indian state or territory.'),
    }

    def clean(self, value):
        value = super(INStateField, self).clean(value)
        if value in EMPTY_VALUES:
            return self.empty_value
        try:
            value = value.strip().lower()
        except AttributeError:
            pass
        else:
            try:
                return str(STATES_NORMALIZED[value.strip().lower()])
            except KeyError:
                pass
        raise ValidationError(self.error_messages['invalid'])


class INStateSelect(Select):
    """
    A Select widget that uses a list of Indian states/territories as its choices.

    .. versionchanged:: 1.1

       Added Telangana to list of states. More details at
       https://en.wikipedia.org/wiki/Telangana#Bifurcation_of_Andhra_Pradesh

    """

    def __init__(self, attrs=None):
        super(INStateSelect, self).__init__(attrs, choices=STATE_CHOICES)
