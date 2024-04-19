# -*- coding: utf-8 -*-
"""Maltese-specific validation helpers."""
from __future__ import unicode_literals

from localflavor.base import RegexValidator
from localflavor.stub import _


class MTPostalCodeField(RegexValidator):
    """
    A form field that validates its input as a Maltese postal code.

    Maltese postal code is a seven digits string, with first three
    being letters and the final four numbers.
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in format XXX NNNN.'),
    }

    def __init__(self, *args, **kwargs):
        super(MTPostalCodeField, self).__init__(r'^[A-Z]{3}\ \d{4}$', *args, **kwargs)
