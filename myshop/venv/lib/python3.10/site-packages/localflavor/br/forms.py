# -*- coding: utf-8 -*-
"""BR-specific validation helpers."""

from __future__ import unicode_literals

import re

from localflavor.stub import EMPTY_VALUES
from localflavor.exceptions import ValidationError
from localflavor.base import CharValidator, RegexValidator, Select
from localflavor.stub import _

from .br_states import STATE_CHOICES

cpf_digits_re = re.compile(r'^(\d{3})\.(\d{3})\.(\d{3})-(\d{2})$')
cnpj_digits_re = re.compile(
    r'^(\d{2})[.-]?(\d{3})[.-]?(\d{3})/(\d{4})-(\d{2})$'
)
process_digits_re = re.compile(
    r'^(\d{7})-?(\d{2})\.?(\d{4})\.?(\d)\.?(\d{2})\.?(\d{4})$'
)


class BRPostalCodeField(RegexValidator):
    """A form field that validates input as a Brazilian zip code, with the format XXXXX-XXX."""

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXXXX-XXX.'),
    }

    def __init__(self, *args, **kwargs):
        super(BRPostalCodeField, self).__init__(r'^\d{5}-\d{3}$', *args, **kwargs)


class BRStateSelect(Select):
    """A Select that uses a list of Brazilian states/territories as its choices."""

    def __init__(self, attrs=None):
        super(BRStateSelect, self).__init__(attrs, choices=STATE_CHOICES)


class BRStateChoiceField(CharValidator):
    """A choice field that uses a list of Brazilian states as its choices."""

    default_error_messages = {
        'invalid': _('Select a valid brazilian state. That state is not one of the available states.'),
    }

    def __init__(self, **kwargs):
        super(BRStateChoiceField, self).__init__(**kwargs)
        self.choices = STATE_CHOICES

    def clean(self, value):
        value = super(BRStateChoiceField, self).clean(value)
        if value in EMPTY_VALUES:
            value = ''
        value = str(value)
        if value == '':
            return value
        valid_values = set([str(entry[0]) for entry in self.choices])
        if value not in valid_values:
            raise ValidationError(self.error_messages['invalid'])
        return value
