import re
from .exceptions import ValidationError


class CharValidator(object):
    """Validates and cleans a given string value of given min/max length."""

    default_error_messages = {
        'invalid': 'Invalid value.'
    }
    empty_values = (None, '')
    empty_value = None
    validators = []
    default_validators = []
    choices = None

    def __init__(self, min_length=None, max_length=None, choices=None, **kwargs):
        self.min_length = min_length
        self.max_length = max_length

        self.choices = choices if choices else self.choices
        self.choices = [str(_[0]) for _ in self.choices] if self.choices else self.choices

        self.error_messages = self.default_error_messages
        if 'message' in kwargs:
            self.error_messages = {'invalid': kwargs.pop('message')}
        self.error_messages = kwargs.pop('error_messages', self.error_messages)

    def _is_valid(self, value):
        if not isinstance(value, str):
            return False
        if self.min_length and len(value) < self.min_length:
            return False
        if self.max_length and len(value) > self.max_length:
            return False
        if self.choices and str(value) not in self.choices:
            return False
        for validator in self.validators + self.default_validators:
            if not validator(value):
                return False
        return True

    def __call__(self, value):
        if not self._is_valid(value):
            raise ValidationError(self.error_messages['invalid'])

    def clean(self, value):
        value = value.strip()
        if value in self.empty_values:
            return self.empty_value

        if not self._is_valid(value):
            raise ValidationError(self.error_messages['invalid'])
        return value


class RegexValidator(CharValidator):
    """Validates and cleans a given value with a given regex."""

    regex = None

    def __init__(self, regex, message=None, *args, **kwargs):
        if message:
            kwargs['message'] = message
        super(RegexValidator, self).__init__(*args, **kwargs)
        self.regex = re.compile(regex)

    def _is_valid(self, value):
        if not super(RegexValidator, self)._is_valid(value):
            return False
        if not self.regex.search(value):
            return False
        return True

    def clean(self, value):
        value = super(RegexValidator, self).clean(value)
        if not self._is_valid(value):
            raise ValidationError(self.error_messages['invalid'])
        return value


class ChoiceField(CharValidator):
    """A stub choice field."""

    pass


class Select(object):
    """A stub select class."""

    def __init__(self, choices=None):
        self.choices = choices
