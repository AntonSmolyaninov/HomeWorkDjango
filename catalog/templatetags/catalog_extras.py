from django import template

register = template.Library()

@register.filter
def get_field_label(form, field_name):
    """Возвращает метку поля формы"""
    try:
        return form[field_name].label
    except (KeyError, AttributeError):
        return field_name
