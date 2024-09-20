from django import template

register = template.Library()

@register.filter
def get_item(dictionary, args):
    row, col = args.split(',')
    return dictionary.get((int(row), int(col)))  # Convert to integers and return seat from dictionary
