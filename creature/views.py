from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from .utils import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'},
        ]


class CreatureHome(DataMixin, ListView):
    paginate_by = 5
    model = Creature
    template_name = 'creature/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Home page")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Creature.objects.filter(is_published=True).select_related('cat')

# def index(request):
#
#     context = {
#         'menu': menu,
#         'title': "Главные ворота",
#     }
#     return render(request, 'creature/index.html', context)

def about(request):
    contact_list = Creature.objects.all()
    paginator = Paginator(contact_list, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'creature/about.html', {'page_obj': page_obj, 'menu': menu, 'title': "Aboute us"})

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

class ShowPost(DataMixin, DeleteView):
    model = Creature
    template_name = 'creature/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context["post"])
        return dict(list(context.items()) + list(c_def.items()))


# def showposts(request, post_slug):
#     post = get_object_or_404(Creature, slug=post_slug)
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'selected': post.slug,
#     }
#     return render(request, 'creature/post.html', context)


class CreatureCategory(DataMixin, ListView):
    paginate_by = 5
    model = Creature
    template_name = 'creature/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Creature.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Category - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

# def show_category(request, cat_slug):
#     # posts = Creature.objects.filter(cat_id=cat_id)
#
#     # if len(posts) == 0:
#     #     raise Http404()
#
#     context = {
#         # 'posts': posts,
#         'menu': menu,
#         'title': "Показ по категории",
#         'selected': cat_slug,
#     }
#     return render(request, 'creature/index.html', context)


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'creature/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Adding an article")
        return dict(list(context.items()) + list(c_def.items()))

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#
#     else:
#         form = AddPostForm()
#     return render(request, 'creature/addpage.html', {'form': form, 'menu': menu, 'title': 'Adding an article'})

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'creature/contact.html'
    success_url = reverse_lazy('home')

    def get_user_context(self, **kwargs):
        context = super().get_user_context(**kwargs)
        c_def = self.get_user_context(title='Feedback')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

# def login(request):
#     pass
#
# def hui(request):
#     pass


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'creature/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Sign up')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'creature/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Login")
        return dict(list(context.items()) + list(c_def.items()))

    # def get_success_url(self):
    #     return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')