from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime
from django.shortcuts import render, render_to_response
from core.models import Project, Task, Timer
from core.models import start_task, stop_task, stop_fast_task, choise_action_yourtasks
from core.models import stop_fast_task, choise_action_fast_task, start_fast_task
from core.models import search_existing_project, search_task


def home(request):
    c = request.user
    pr = Project.objects.all()
    if request.method == 'POST':
        alldata = request.POST
        taskname = alldata.get("taskname")
        taskdescription = alldata.get("taskdescription")
        projectname = alldata.get("projectname")
        p = Project.objects.get(name = projectname)
        t = Task(name = taskname, description = taskdescription, user = c, project = p)
        t.save()
    return render(request, 'home.html', {'projects':pr, 'user':c})

def projects(request):
    if request.method == 'POST':
        alldata=request.POST
        projectname = alldata.get("projectname")
        projectcost = alldata.get("projectcost")
        p=Project(name = projectname, price_per_hour = projectcost)
        p.save()
    return render(request, 'projects.html')

def search_task(request):
    if Task.objects.filter(name = "in_progress",user = request.user):
        return Task.objects.filter(name = "in_progress", user=request.user)
    else:
        return None

def yourtasks(request):    
    last_task = search_task(request)
    if request.method == 'POST':
        alldata = request.POST           
        choise_action_yourtasks(Task.objects.get(id = alldata.get("task_selected")), alldata.get("choisebuttom"))
        return HttpResponseRedirect('/yourtasks') 
    tasks = request.user.task_set.all().order_by('project__name')
    return render(request, 'yourtasks.html', {'tasks':tasks, 'last_task':last_task})


def fast_task(request):
    if request.method == 'POST':
        tupla = choise_action_fast_task(request.POST.get("choisebuttom"),request.POST, request.user)
        return HttpResponseRedirect('/yourtasks') 