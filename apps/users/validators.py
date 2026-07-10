import re
from django.core.exceptions import ValidationError

class PasswordValidator:
    def __init__(self, field) -> None:
        self.field = field

    def __call__(self, value):
        reg_pattern = re.compile(r'^[A-Za-z0-9]+$')
        tmp_value = dict(value).get(self.field)
        if not bool(reg_pattern.match(tmp_value)):
            raise ValidationError('Ошибка: пароль должен содержать только латинские буквы и цифры')