from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect


# Create your views here.


def index(request):
    return render(request, 'creature/index.html')

def about(request):
    return render(request, 'creature/about.html')

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