from django import template
from django.http import Http404

from creature.models import *

register = template.Library()
#
#
# @register.simple_tag(name="getcats")
# def get_categories(filter=None):
#     if not filter:
#         return Category.objects.all()
#     else:
#         return Category.objects.filter(pk=filter)
#
# @register.inclusion_tag('creature/list_categories.html')
# def show_categories(sort=None, cat_selected=0):
#     if not sort:
#         cats = Category.objects.all()
#     else:
#         cats = Category.objects.order_by(sort)
#     print(cat_selected)
#     # print("--------------------------")
#     if cat_selected:
#         cat_selected = Category.objects.get(name=cat_selected).pk
#     return {"cats": cats, 'selected': cat_selected}
#
# @register.inclusion_tag('creature/list_creatures.html')
# def show_posts(cat_id=None, sort=None):
#     # print(f"--{cat_id}--")
#     if not cat_id:
#         posts = Creature.objects.filter(is_published=True)
#     else:
#
#         posts = Creature.objects.filter(cat_id=cat_id, is_published=True)
#         print(posts)
#     if len(posts) == 0:
#         raise Http404()
#
#     return {"posts": posts, "selected": cat_id}
