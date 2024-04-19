"""USA-specific validation helpers."""

from __future__ import unicode_literals

from localflavor.stub import EMPTY_VALUES
from localflavor.exceptions import ValidationError
from localflavor.base import CharValidator, RegexValidator, Select
from localflavor.stub import _


class USZipCodeField(RegexValidator):
    """
    A form field that validates input as a U.S. ZIP code.

    Valid formats are XXXXX or XXXXX-XXXX.

    .. note::

        If you are looking for a form field with a list of U.S. Postal Service
        locations please use :class:`~localflavor.us.forms.USPSSelect`.

    .. versionadded:: 1.1

    Whitespace around the ZIP code is accepted and automatically trimmed.
    """

    default_error_messages = {
        'invalid': _('Enter a valid ZIP code in the format XXXXX or XXXXX-XXXX.'),
    }

    def __init__(self, *args, **kwargs):
        super(USZipCodeField, self).__init__(r'^\d{5}(?:-\d{4})?$', *args, **kwargs)


class USStateField(CharValidator):
    """
    A form field that validates its input is a U.S. state, territory, or COFA territory.

    The input is validated against a dictionary which includes names and abbreviations.
    It normalizes the input to the standard two-letter postal service
    abbreviation for the given state.
    """

    default_error_messages = {
        'invalid': _('Enter a U.S. state or territory.'),
    }

    def clean(self, value):
        from .us_states import STATES_NORMALIZED
        super(USStateField, self).clean(value)
        if value in EMPTY_VALUES:
            return self.empty_value
        try:
            value = value.strip().lower()
        except AttributeError:
            pass
        else:
            try:
                return STATES_NORMALIZED[value.strip().lower()]
            except KeyError:
                pass
        raise ValidationError(self.error_messages['invalid'])


class USStateSelect(Select):
    """A Select widget that uses a list of U.S. states/territories as its choices."""

    def __init__(self, attrs=None):
        from .us_states import STATE_CHOICES
        super(USStateSelect, self).__init__(attrs, choices=STATE_CHOICES)


class USPSSelect(Select):
    """
    A Select widget that uses a list of US Postal Service codes as its choices.

    .. note::

        If you are looking for a form field that validates U.S. ZIP codes
        please use :class:`~localflavor.us.forms.USZipCodeField`.

    """

    def __init__(self, attrs=None):
        from .us_states import USPS_CHOICES
        super(USPSSelect, self).__init__(attrs, choices=USPS_CHOICES)
