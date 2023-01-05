from wtforms import SubmitField, RadioField, MultipleFileField
from wtforms.csrf.core import CSRFTokenField


service_fields = (CSRFTokenField, SubmitField)


def set_values_to_form(form, values):
    for field in form:
        try:
            if isinstance(field, RadioField):
                field.data = int(values[field.name])
            else:
                field.data = values[field.name]
        except:
            continue


def get_values_from_form(form):
    values = {}
    for field in form:
        if not isinstance(field, service_fields):
            if isinstance(field, MultipleFileField):
                if field.data[0].filename:
                    values[field.name] = field.data
                else:
                    values[field.name] = ''
            else:
                values[field.name] = field.data
    return values
