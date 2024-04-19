# -*- coding: utf-8 -*-
"""FR-specific validation helpers."""
from __future__ import unicode_literals


from localflavor.base import RegexValidator
from localflavor.stub import _


class FRPostalCodeField(RegexValidator):
    """
    Validate local French zip code.

    The correct format is 'XXXXX'.
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXXXX.'),
    }

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 5
        kwargs['min_length'] = 5
        super(FRPostalCodeField, self).__init__(r'^\d{5}$', *args, **kwargs)
