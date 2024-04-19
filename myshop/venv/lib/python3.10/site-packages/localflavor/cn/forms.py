"""China(mainland)-specific validation helpers."""

from __future__ import unicode_literals

from localflavor.base import RegexValidator, Select
from localflavor.stub import _

from .cn_provinces import PROVINCE_CHOICES

__all__ = (
    'CNProvinceSelect',
    'CNPostalCodeField',
)


ID_CARD_RE = r'^\d{15}(\d{2}[0-9xX])?$'
POST_CODE_RE = r'^\d{6}$'

# Valid location code used in id card checking algorithm
CN_LOCATION_CODES = (
    11,  # Beijing
    12,  # Tianjin
    13,  # Hebei
    14,  # Shanxi
    15,  # Nei Mongol
    21,  # Liaoning
    22,  # Jilin
    23,  # Heilongjiang
    31,  # Shanghai
    32,  # Jiangsu
    33,  # Zhejiang
    34,  # Anhui
    35,  # Fujian
    36,  # Jiangxi
    37,  # Shandong
    41,  # Henan
    42,  # Hubei
    43,  # Hunan
    44,  # Guangdong
    45,  # Guangxi
    46,  # Hainan
    50,  # Chongqing
    51,  # Sichuan
    52,  # Guizhou
    53,  # Yunnan
    54,  # Xizang
    61,  # Shaanxi
    62,  # Gansu
    63,  # Qinghai
    64,  # Ningxia
    65,  # Xinjiang
    71,  # Taiwan
    81,  # Hong Kong
    91,  # Macao
)


class CNProvinceSelect(Select):
    """A select widget providing the list of provinces and districts in People's Republic of China as choices."""

    def __init__(self, attrs=None):
        super(CNProvinceSelect, self).__init__(attrs, choices=PROVINCE_CHOICES)


class CNPostalCodeField(RegexValidator):
    """
    A form field that validates input as postal codes in mainland China.

    Valid codes are in the format of XXXXXX where X is a digit.
    """

    default_error_messages = {
        'invalid': _('Enter a valid postal code in the format XXXXXX.'),
    }

    def __init__(self, *args, **kwargs):
        super(CNPostalCodeField, self).__init__(POST_CODE_RE, *args, **kwargs)
