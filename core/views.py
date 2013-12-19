from django.http import HttpResponse,Http404
import datetime
from django.shortcuts import render, render_to_response
from core.models import UserProfile, Project, Task, Timer
from core.models import start_task, stop_task, stop_fast_task, first_div
from core.models import stop_second_div, second_div, start_second_div
from core.models import search_existing_project

def home(request):
    c = UserProfile.objects.all()[0]
    pr = Project.objects.all()
    if request.method == 'POST':
        alldata = request.POST
        taskname = alldata.get("taskname")
        taskdescription = alldata.get("taskdescription")
        projectname = alldata.get("projectname")
        p = Project.objects.get(name = projectname)
        t = Task(name = taskname, description = taskdescription, user = c, project = p)
        t.save()
    return render(request, 'home.html', {'projects':pr})

def projects(request):
    if request.method == 'POST':
        alldata=request.POST
        projectname = alldata.get("projectname")
        projectcost = alldata.get("projectcost")
        p=Project(name = projectname, price_per_hour = projectcost)
        p.save()
    return render(request, 'projects.html')


def yourtasks(request):
    if request.method == 'POST':
        alldata = request.POST           
        first_div(Task.objects.get(id = alldata.get("task_selected")), alldata.get("choisebuttom"))
    tasks = UserProfile.objects.all()[0].task_set.all().order_by('project__name')
    return render(request, 'yourtasks.html', {'tasks':tasks, 'last_task':None, 'message':''})

def fast_task(request):
    last_task = None
    msg = ""
    if request.method == 'POST':
        tupla = second_div(request.POST.get("choisebuttom"),request.POST)
        last_task = tupla[0]
        msg = tupla[1]
    tasks = UserProfile.objects.all()[0].task_set.all().order_by('project__name')
    return render(request, 'yourtasks.html', {'tasks':tasks, 'last_task':last_task, 'message':msg})