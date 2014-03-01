from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime
from django.shortcuts import render, render_to_response
from core.models import Project, Task, Timer
from core.models import start_task, stop_task, stop_fast_task, choise_action_yourtasks
from core.models import stop_fast_task, choise_action_fast_task, start_fast_task
from core.models import search_existing_project, search_task

def home(request):
    return content_home(request)

def create_task(request, project):
    task_name = request.POST.get("taskname")
    task_description = request.POST.get("taskdescription")
    t = Task(name=task_name, description=task_description, user=request.user, project=project)
    t.save()

def create_project(request):
    project_name = request.POST.get("projectname")
    project_cost = request.POST.get("projectcost")
    p = Project(name=project_name, price_per_hour=project_cost)
    p.save()

def content_home(request):
    if request.method == 'POST':
        p = Project.objects.get(name = request.POST.get("projectname"))
        create_task(request,p)
    return render(request, 'home.html', {'projects':Project.objects.all(), 'user':request.user})

def projects(request):
    return content_projects(request)

def content_projects(request):
    if request.method == 'POST':
        create_project(request)
    return render(request, 'projects.html')

def yourtasks(request):
    return content_yourtasks(request)

def content_yourtasks(request):
    last_task = search_task(request)
    if request.method == 'POST':
        alldata = request.POST
        choise_action_yourtasks(Task.objects.get(id = alldata.get("task_selected")), alldata.get("choisebuttom"))
        return HttpResponseRedirect('/yourtasks')
    tasks = request.user.task_set.all().order_by('project__name')
    return render(request, 'yourtasks.html', {'tasks':tasks, 'last_task':last_task})


def yourtasks_current_month(request):
    return content_yourtasks_current_month(request)

def content_yourtasks_current_month(request):
    last_task = search_task(request)
    if request.method == 'POST':
        alldata = request.POST
        choise_action_yourtasks(Task.objects.get(id = alldata.get("task_selected")), alldata.get("choisebuttom"))
        return HttpResponseRedirect('/yourtasks/current_month')
    tasks = request.user.task_set.current_month_tasks()
    return render(request, 'yourtasks.html', {'tasks':tasks, 'last_task':last_task})


def fast_task(request):
    return content_fast_task(request)

def content_fast_task(request):
    if request.method == 'POST':
        choise_action_fast_task(request.POST.get("choisebuttom"),request.POST, request.user)
        return HttpResponseRedirect('/yourtasks')

class AuthenticationMiddleware(object):
    def process_request(self, request):
        if not '/accounts/' in request.get_full_path() and request.user.is_anonymous():
            return HttpResponseRedirect('/accounts/login/')
        return None
