from localflavor.base import RegexValidator, CharValidator
from localflavor.exceptions import ValidationError
from unittest import TestCase


class RegexValidatorTest(TestCase):
    def test_regex_validator(self):
        validator = RegexValidator(r'^\d{10}$', 'Test error message')
        validator('1234567890')
        with self.assertRaises(ValidationError):
            validator('asdfasdf')


class CharValidatorTest(TestCase):
    def test_char_validator(self):
        validator = CharValidator(min_length=2, max_length=4)
        validator('333')
        with self.assertRaises(ValidationError):
            validator('11111')
