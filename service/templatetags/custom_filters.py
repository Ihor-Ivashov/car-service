from django.template.defaulttags import register


@register.filter
def get_item(form, key):
    field = form.fields.get(key)
    return field.get_bound_field(form, key)
