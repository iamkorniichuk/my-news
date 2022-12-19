from wtforms import SubmitField
from wtforms.csrf.core import CSRFTokenField


service_fields = (CSRFTokenField, SubmitField)


def set_values_to_form(form, values):
    for field in form:
        try:
            field.data = values[field.name]
        except:
            continue


def get_values_from_form(form):
    values = {}
    for field in form:
        if not isinstance(field, service_fields):
            values[field.name] = field.data
    return values
