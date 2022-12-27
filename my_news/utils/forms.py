from wtforms import SubmitField, FileField
from wtforms.csrf.core import CSRFTokenField


service_fields = (CSRFTokenField, SubmitField)


def set_values_to_form(form, values):
    for field in form:
        try:
            if isinstance(field, FileField):
                # TODO: TO end
                field.data = open(values[field.name], 'r')
            else:
                field.data = values[field.name]
        except:
            continue


def get_values_from_form(form):
    values = {}
    for field in form:
        if not isinstance(field, service_fields):
            values[field.name] = field.data
    return values
