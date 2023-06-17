from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .models import *
# Create your views here.

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'},
        ]

def index(request):

    context = {
        'menu': menu,
        'title': "Главные ворота",
    }
    return render(request, 'creature/index.html', context)

def about(request):
    return render(request, 'creature/about.html', context)

def categories(request, cat):
    if request.POST:
        print(request.POST)

    return HttpResponse(f"<h1> Categories </h1><p> {cat} </p>")


def archive(request, year):
    if int(year) > 2023:
        return redirect('home', permanent=True)
        # raise Http404()
    return HttpResponse(f"<h1> Archive on years </h1> <p> {year} </p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1> idi na hui</h1>")


def showposts(request, post_slug):
    post = get_object_or_404(Creature, slug=post_slug)
    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        'selected': post.slug,
    }
    return render(request, 'creature/post.html', context)

def show_category(request, cat_slug):
    # posts = Creature.objects.filter(cat_id=cat_id)

    # if len(posts) == 0:
    #     raise Http404()

    context = {
        # 'posts': posts,
        'menu': menu,
        'title': "Показ по категории",
        'selected': cat_slug,
    }
    return render(request, 'creature/index.html', context)


def addpage(request):
    return render(request, 'creature/addpage.html', {'menu': menu, 'title': 'Adding an article'})

def contact(request):
    pass

def login(request):
    pass

def hui(request):
    pass