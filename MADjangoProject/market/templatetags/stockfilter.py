from django import template

register = template.Library()

@register.filter(name='has_user')
def has_user(model, usr):
    # if collection have user entry
    return model.filter(user=usr).exists()
