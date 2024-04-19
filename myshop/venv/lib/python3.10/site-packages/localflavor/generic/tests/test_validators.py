from unittest import TestCase
from ...base import ValidationError
from ..validators import validate_country_postcode


class PostcodeValidatorsPerCountryTest(TestCase):
    def test_validate_postcode_ar(self):
        validate_country_postcode('1234', 'AR')
        validate_country_postcode('A1234AAA', 'AR')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format NNNN or ANNNNAAA.'):
            validate_country_postcode('AB 1234', 'AR')

    def test_validate_postcode_at(self):
        validate_country_postcode('1234', 'AT')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXX.'):
            validate_country_postcode('AB 1234', 'AT')

    def test_validate_postcode_au(self):
        validate_country_postcode('1234', 'AU')

        with self.assertRaisesRegex(ValidationError, 'Enter a 4 digit postal code.'):
            validate_country_postcode('AB 1234', 'AU')

    def test_validate_postcode_be(self):
        validate_country_postcode('1234', 'BE')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the range and format 1XXX - 9XXX.'):
            validate_country_postcode('AB 1234', 'BE')

    def test_validate_postcode_br(self):
        validate_country_postcode('12345-111', 'BR')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXX-XXX.'):
            validate_country_postcode('AB 1234', 'BR')

    def test_validate_postcode_ca(self):
        validate_country_postcode('A1C 1A2', 'CA')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXX XXX.'):
            validate_country_postcode('AB 1234', 'CA')

    def test_validate_postcode_ch(self):
        validate_country_postcode('1234', 'CH')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the range and format 1XXX - 9XXX.'):
            validate_country_postcode('AB 1234', 'CH')

    def test_validate_postcode_cn(self):
        validate_country_postcode('123456', 'CN')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXXX.'):
            validate_country_postcode('AB 1234', 'CN')

    def test_validate_postcode_cu(self):
        validate_country_postcode('12345', 'CU')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXX.'):
            validate_country_postcode('AB 1234', 'CU')

    def test_validate_postcode_cz(self):
        validate_country_postcode('123 45', 'CZ')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXX or XXX XX.'):
            validate_country_postcode('AB 1234', 'CZ')

    def test_validate_postcode_de(self):
        validate_country_postcode('12345', 'DE')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXX.'):
            validate_country_postcode('AB 1234', 'DE')

    def test_validate_postcode_dk(self):
        validate_country_postcode('0555', 'DK')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXX.'):
            validate_country_postcode('AB 1234', 'DK')

    def test_validate_postcode_ee(self):
        validate_country_postcode('12345', 'EE')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXX.'):
            validate_country_postcode('AB 1234', 'EE')

    def test_validate_postcode_es(self):
        validate_country_postcode('01234', 'ES')

        with self.assertRaisesRegex(ValidationError,
                                    'Enter a valid postal code in the range and format 01XXX - 52XXX.'):
            validate_country_postcode('53111', 'ES')

    def test_validate_postcode_fi(self):
        validate_country_postcode('12345', 'FI')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXX.'):
            validate_country_postcode('AB 1234', 'FI')

    def test_validate_postcode_fr(self):
        validate_country_postcode('12345', 'FR')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXX.'):
            validate_country_postcode('AB 1234', 'FR')

    def test_validate_postcode_gb(self):
        validate_country_postcode('M1 1AE', 'GB')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code.'):
            validate_country_postcode('AB 1234', 'GB')

    def test_validate_postcode_gr(self):
        validate_country_postcode('12345', 'GR')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid 5-digit postal code.'):
            validate_country_postcode('AB 1234', 'GR')

    def test_validate_postcode_hr(self):
        validate_country_postcode('12345', 'HR')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid 5 digit postal code.'):
            validate_country_postcode('AB 1234', 'HR')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid 5 digit postal code.'):
            validate_country_postcode('60001', 'HR')

    def test_validate_postcode_id(self):
        validate_country_postcode('12340', 'ID')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid 5 digit postal code.'):
            validate_country_postcode('AB 1234', 'ID')

    def test_validate_postcode_il(self):
        validate_country_postcode('1234567', 'IL')
        validate_country_postcode('12345', 'IL')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXXXX or XXXXX'):
            validate_country_postcode('AB 1234', 'IL')

    def test_validate_postcode_in(self):
        validate_country_postcode('123456', 'IN')
        validate_country_postcode('123 456', 'IN')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXXX or XXX XXX.'):
            validate_country_postcode('AB 1234', 'IN')

    def test_validate_postcode_is(self):
        validate_country_postcode('123', 'IS')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid 3 digit postal code.'):
            validate_country_postcode('AB 1234', 'IS')

    def test_validate_postcode_it(self):
        validate_country_postcode('12345', 'IT')

        with self.assertRaisesRegex(ValidationError, 'Enter a 5 digit ZIP code.'):
            validate_country_postcode('AB 1234', 'IT')

    def test_validate_postcode_jp(self):
        validate_country_postcode('123-4567', 'JP')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXXXX or XXX-XXXX.'):
            validate_country_postcode('AB 1234', 'JP')

    def test_validate_postcode_lt(self):
        validate_country_postcode('LT-12345', 'LT')
        validate_country_postcode('12345', 'LT')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXX or LT-XXXXX.'):
            validate_country_postcode('1234', 'LT')

    def test_validate_postcode_lv(self):
        validate_country_postcode('LV-1234', 'LV')
        validate_country_postcode('1234', 'LV')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXX or LV-XXXX.'):
            validate_country_postcode('AB 1234', 'LV')

    def test_validate_postcode_ma(self):
        validate_country_postcode('12345', 'MA')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXX.'):
            validate_country_postcode('AB 1234', 'MA')

    def test_validate_postcode_mt(self):
        validate_country_postcode('ABC 1234', 'MT')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in format XXX NNNN.'):
            validate_country_postcode('1234', 'MT')

    def test_validate_postcode_mx(self):
        validate_country_postcode('01162', 'MX')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXX.'):
            validate_country_postcode('17345', 'MX')

    def test_validate_postcode_nl(self):
        validate_country_postcode('1234 AB', 'NL')
        assert validate_country_postcode('1234 ab', 'NL') == '1234 AB'

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format NNNN XX.'):
            validate_country_postcode('AB 1234', 'NL')

    def test_validate_postcode_no(self):
        validate_country_postcode('1234', 'NO')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXX.'):
            validate_country_postcode('AB 1234', 'NO')

    def test_validate_postcode_nz(self):
        validate_country_postcode('1234', 'NZ')

        with self.assertRaisesRegex(ValidationError, 'Enter a 4 digit postal code.'):
            validate_country_postcode('12345', 'NZ')

    def test_validate_postcode_pk(self):
        validate_country_postcode('12345', 'PK')

        with self.assertRaisesRegex(ValidationError, 'Enter a 5 digit postal code.'):
            validate_country_postcode('AB123', 'PK')

    def test_validate_postcode_pl(self):
        validate_country_postcode('12-344', 'PL')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XX-XXX.'):
            validate_country_postcode('12341', 'PL')

    def test_validate_postcode_pt(self):
        validate_country_postcode('9245-222', 'PT')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XYYY-YYY'):
            validate_country_postcode('AB 1234', 'PT')

    def test_validate_postcode_ro(self):
        validate_country_postcode('123456', 'RO')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXXX.'):
            validate_country_postcode('999234', 'RO')

    def test_validate_postcode_ru(self):
        validate_country_postcode('123456', 'RU')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXXX.'):
            validate_country_postcode('AB 1234', 'RU')

    def test_validate_postcode_se(self):
        validate_country_postcode('12345', 'SE')

        with self.assertRaisesRegex(ValidationError, 'Enter a Swedish postal code in the format XXXXX or XXX XX.'):
            validate_country_postcode('1234B', 'SE')

    def test_validate_postcode_sg(self):
        validate_country_postcode('123456', 'SG')

        with self.assertRaisesRegex(ValidationError, 'Enter a 6-digit postal code.'):
            validate_country_postcode('1234AA', 'SG')

    def test_validate_postcode_si(self):
        validate_country_postcode('2275', 'SI')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXX.'):
            validate_country_postcode('AB 1234', 'SI')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXX.'):
            validate_country_postcode('9266', 'SI')

    def test_validate_postcode_sk(self):
        validate_country_postcode('12345', 'SK')
        validate_country_postcode('123 45', 'SK')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXX or XXX XX.'):
            validate_country_postcode('AB 1234', 'SK')

    def test_validate_postcode_tr(self):
        validate_country_postcode('12345', 'TR')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXX.'):
            validate_country_postcode('AB 1234', 'TR')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXX.'):
            validate_country_postcode('82345', 'TR')

    def test_validate_postcode_ua(self):
        validate_country_postcode('12345', 'UA')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXX.'):
            validate_country_postcode('00123', 'UA')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid postal code in the format XXXXX.'):
            validate_country_postcode('00123 A', 'UA')

    def test_validate_postcode_us(self):
        validate_country_postcode('12345', 'US')
        validate_country_postcode('12345-1111', 'US')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid ZIP code in the format XXXXX or XXXXX-XXXX.'):
            validate_country_postcode('AB 1234', 'US')

    def test_validate_postcode_za(self):
        validate_country_postcode('1234', 'ZA')

        with self.assertRaisesRegex(ValidationError, 'Enter a valid South African postal code in the format XXXX.'):
            validate_country_postcode('AB 1234', 'ZA')
