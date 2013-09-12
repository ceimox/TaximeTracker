from django.http import HttpResponse,Http404
import datetime
from django.shortcuts import render, render_to_response

def showindex(request):
    return render(request, 'show.html',{'img':'index.png'})

def showhome(request):
    return render(request, 'show.html',{'img':'home.png'})

def home(request):
    return render(request, 'home.html')

def showregistration(request):
    return render(request, 'show.html',{'img':'registration.png'})

def showalltasks(request):
    return render(request, 'show.html',{'img':'alltasks.png'})

def showprojects(request):
    return render(request, 'show.html',{'img':'projects.png'})

def showallprojects(request):
    return render(request, 'show.html',{'img':'allprojects.png'})        