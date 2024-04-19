from __future__ import unicode_literals

import re

from localflavor.base import RegexValidator, Select
from localflavor.stub import _

from .ee_counties import COUNTY_CHOICES

zipcode = re.compile(r'^[1-9]\d{4}$')


class EEPostalCodeField(RegexValidator):
    """
    A form field that validates input as a Estonian zip code.

    Valid codes consist of five digits; first digit cannot be 0.
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXXXX.'),
    }

    def __init__(self, *args, **kwargs):
        super(EEPostalCodeField, self).__init__(zipcode, *args, **kwargs)


class EECountySelect(Select):
    """A Select widget that uses a list of Estonian counties as its choices."""

    def __init__(self, attrs=None):
        super(EECountySelect, self).__init__(attrs, choices=COUNTY_CHOICES)
