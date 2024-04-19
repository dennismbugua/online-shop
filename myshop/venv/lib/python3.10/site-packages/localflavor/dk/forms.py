"""Denmark specific validation helpers."""

from __future__ import unicode_literals

from localflavor.base import ChoiceField, Select
from localflavor.stub import _

from .dk_municipalities import DK_MUNICIPALITIES
from .dk_postalcodes import DK_POSTALCODES


class DKPostalCodeField(ChoiceField):
    """An Input widget that uses a list of Danish postal codes as valid input."""

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXXX.')
    }
    choices = DK_POSTALCODES


class DKMunicipalitySelect(Select):
    """A Select widget that uses a list of Danish municipalities (kommuner) as its choices."""

    def __init__(self, attrs=None, *args, **kwargs):
        super(DKMunicipalitySelect, self).__init__(
            attrs,
            choices=DK_MUNICIPALITIES,
            *args,
            **kwargs
        )
