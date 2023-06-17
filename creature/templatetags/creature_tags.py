from django import template
from django.http import Http404

from creature.models import *

register = template.Library()


@register.simple_tag(name="getcats")
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)

@register.inclusion_tag('creature/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {"cats": cats, 'selected': cat_selected}

@register.inclusion_tag('creature/list_creatures.html')
def show_posts(cat_slug=None, sort=None):
    print(f"--{cat_slug}--")
    if not cat_slug:
        posts = Creature.objects.all()
    else:
        cat_id = Category.objects.get(slug=cat_slug)
        posts = Creature.objects.filter(cat_id=cat_id)
        print(posts)
    if len(posts) == 0:
        raise Http404()

    return {"posts": posts}
