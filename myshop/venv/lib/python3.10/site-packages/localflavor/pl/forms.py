"""Polish-specific form helpers."""

from __future__ import unicode_literals

from localflavor.base import RegexValidator, Select
from localflavor.stub import _

from .pl_administrativeunits import ADMINISTRATIVE_UNIT_CHOICES
from .pl_voivodeships import VOIVODESHIP_CHOICES


class PLProvinceSelect(Select):
    """A select widget with list of Polish administrative provinces as choices."""

    def __init__(self, attrs=None):
        super(PLProvinceSelect, self).__init__(attrs, choices=VOIVODESHIP_CHOICES)


class PLCountySelect(Select):
    """A select widget with list of Polish administrative units as choices."""

    def __init__(self, attrs=None):
        super(PLCountySelect, self).__init__(attrs, choices=ADMINISTRATIVE_UNIT_CHOICES)


class PLPostalCodeField(RegexValidator):
    """
    A form field that validates as Polish postal code.

    Valid code is XX-XXX where X is digit.
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XX-XXX.'),
    }

    def __init__(self, *args, **kwargs):
        super(PLPostalCodeField, self).__init__(r'^\d{2}-\d{3}$', *args, **kwargs)
