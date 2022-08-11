from django.core.validators import MaxValueValidator


def current_year():
    return current_year


def current_year_validator(value):
    value = current_year()
    return MaxValueValidator(value)
