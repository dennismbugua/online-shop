from .ar.ar_provinces import PROVINCE_CHOICES as AR_PROVINCE_CHOICES
from .at.at_states import STATE_CHOICES as AT_STATE_CHOICES
from .au.au_states import STATE_CHOICES as AU_STATE_CHOICES
from .be.be_provinces import PROVINCE_CHOICES as BE_PROVINCE_CHOICES
from .br.br_states import STATE_CHOICES as BR_STATE_CHOICES
from .ca.ca_provinces import PROVINCE_CHOICES as CA_PROVINCE_CHOICES
from .ch.ch_cantons import CANTON_CHOICES as CH_CANTON_CHOICES
from .cn.cn_provinces import PROVINCE_CHOICES as CN_PROVINCE_CHOICES
from .cz.cz_regions import REGION_CHOICES as CZ_REGION_CHOICES
from .de.de_states import STATE_CHOICES as DE_STATE_CHOICES
from .ee.ee_counties import COUNTY_CHOICES as EE_COUNTY_CHOICES
from .es.es_provinces import PROVINCE_CHOICES as ES_PROVINCE_CHOICES
from .fi.fi_municipalities import MUNICIPALITY_CHOICES as FI_MUNICIPALITY_CHOICES
from .gb.gb_regions import REGION_CHOICES as GB_REGION_CHOICES
from .hr.hr_counties import COUNTY_CHOICES as HR_COUNTY_CHOICES
from .id_.id_provinces import PROVINCE_CHOICES as ID_PROVINCE_CHOICES
from .in_.in_states import STATE_CHOICES as IN_STATE_CHOICES
from .it.it_provinces import PROVINCE_CHOICES as IT_PROVINCE_CHOICES
from .ma.ma_provinces import PROVINCE_CHOICES as MA_PROVINCE_CHOICES
from .mx.mx_states import STATE_CHOICES as MX_STATE_CHOICES
from .nl.nl_provinces import PROVINCE_CHOICES as NL_PROVINCE_CHOICES
from .no.no_municipalities import MUNICIPALITY_CHOICES as NO_MUNICIPALITY_CHOICES
from .nz.nz_provinces import PROVINCE_CHOICES as NZ_PROVINCE_CHOICES
from .pk.pk_states import STATE_CHOICES as PK_STATE_CHOICES
from .pt.pt_regions import REGION_CHOICES as PT_REGION_CHOICES
from .se.se_counties import COUNTY_CHOICES as SE_COUNTY_CHOICES
from .sk.sk_regions import REGION_CHOICES as SK_REGION_CHOICES
from .tr.tr_provinces import PROVINCE_CHOICES as TR_PROVINCE_CHOICES
from .ua.ua_regions import REGION_CHOICES as UA_REGION_CHOICES
from .us.us_states import STATE_CHOICES as US_STATE_CHOICES
from .za.za_provinces import PROVINCE_CHOICES as ZA_PROVINCE_CHOICES


# See http://www.bitboost.com/ref/international-address-formats/
ADMINISTRATIVE_AREAS = {
    'AR': {
        'used_in_address': False,
        'type': 'province',
        'choices': AR_PROVINCE_CHOICES,
    },
    'AT': {
        'used_in_address': False,
        'type': 'state',
        'choices': AT_STATE_CHOICES,
    },
    'AU': {
        'used_in_address': True,
        'type': 'state',
        'choices': AU_STATE_CHOICES,
    },
    'BE': {
        'used_in_address': False,
        'type': 'province',
        'choices': BE_PROVINCE_CHOICES,
    },
    'BR': {
        'used_in_address': True,
        'type': 'state',
        'choices': BR_STATE_CHOICES,
    },
    'CA': {
        'used_in_address': True,
        'type': 'province',
        'choices': CA_PROVINCE_CHOICES,
    },
    'CH': {
        'used_in_address': True,
        'type': 'canton',
        'choices': CH_CANTON_CHOICES,
    },
    'CN': {
        'used_in_address': True,
        'type': 'province',
        'choices': CN_PROVINCE_CHOICES,
    },
    'CZ': {
        'used_in_address': False,
        'type': 'region',
        'choices': CZ_REGION_CHOICES,
    },
    'DE': {
        'used_in_address': False,
        'type': 'state',
        'choices': DE_STATE_CHOICES,
    },
    'EE': {
        'used_in_address': False,
        'type': 'county',
        'choices': EE_COUNTY_CHOICES,
    },
    'ES': {
        'used_in_address': False,
        'type': 'province',
        'choices': ES_PROVINCE_CHOICES,
    },
    'FI': {
        'used_in_address': False,
        'type': 'municipality',
        'choices': FI_MUNICIPALITY_CHOICES,
    },
    'GB': {
        'used_in_address': False,
        'type': 'region',
        'choices': GB_REGION_CHOICES,
    },
    'HR': {
        'used_in_address': False,
        'type': 'county',
        'choices': HR_COUNTY_CHOICES,
    },
    'ID': {
        'used_in_address': False,
        'type': 'province',
        'choices': ID_PROVINCE_CHOICES,
    },
    'IN': {
        'used_in_address': False,
        'type': 'state',
        'choices': IN_STATE_CHOICES,
    },
    'IT': {
        'used_in_address': True,
        'type': 'province',
        'choices': IT_PROVINCE_CHOICES,
    },
    'MA': {
        'used_in_address': False,
        'type': 'province',
        'choices': MA_PROVINCE_CHOICES,
    },
    'MX': {
        'used_in_address': True,
        'type': 'state',
        'choices': MX_STATE_CHOICES,
    },
    'NL': {
        'used_in_address': False,
        'type': 'province',
        'choices': NL_PROVINCE_CHOICES,
    },
    'NO': {
        'used_in_address': False,
        'type': 'municipality',
        'choices': NO_MUNICIPALITY_CHOICES,
    },
    'NZ': {
        'used_in_address': False,
        'type': 'province',
        'choices': NZ_PROVINCE_CHOICES,
    },
    'PK': {
        'used_in_address': False,
        'type': 'state',
        'choices': PK_STATE_CHOICES,
    },
    'PT': {
        'used_in_address': False,
        'type': 'region',
        'choices': PT_REGION_CHOICES,
    },
    'SE': {
        'used_in_address': False,
        'type': 'county',
        'choices': SE_COUNTY_CHOICES,
    },
    'SK': {
        'used_in_address': False,
        'type': 'region',
        'choices': SK_REGION_CHOICES,
    },
    'TR': {
        'used_in_address': False,
        'type': 'province',
        'choices': TR_PROVINCE_CHOICES,
    },
    'UA': {
        'used_in_address': False,
        'type': 'region',
        'choices': UA_REGION_CHOICES,
    },
    'US': {
        'used_in_address': True,
        'type': 'state',
        'choices': US_STATE_CHOICES,
    },
    'ZA': {
        'used_in_address': False,
        'type': 'province',
        'choices': ZA_PROVINCE_CHOICES,
    },
}
