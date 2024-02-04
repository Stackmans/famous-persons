from django import template
from women.models import Category  # Змінено імпорт

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected=0):
    categories = Category.objects.all()  # Виправлено тут
    return {'categories': categories, 'cat_selected': cat_selected}
