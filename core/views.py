from django.http import HttpResponse,Http404
import datetime
from django.shortcuts import render, render_to_response
from core.models import UserProfile, Project, Task, Timer

def showindex(request):
    return render(request, 'show.html',{'img':'index.png'})

def showhome(request):
    return render(request, 'show.html',{'img':'home.png'})

def showregistration(request):
    return render(request, 'show.html',{'img':'registration.png'})

def showalltasks(request):
    return render(request, 'show.html',{'img':'alltasks.png'})

def showprojects(request):
    return render(request, 'show.html',{'img':'projects.png'})

def showallprojects(request):
    return render(request, 'show.html',{'img':'allprojects.png'})

def home(request):
    c=UserProfile.objects.all()[0]
    pr=Project.objects.all()
    if request.method == 'POST':
        alldata=request.POST
        taskname = alldata.get("taskname")
        taskdescription = alldata.get("taskdescription")
        projectname= alldata.get("projectname")
        p=Project.objects.get(name=projectname)
        t=Task(name=taskname,description=taskdescription,user=c,project=p)
        t.save()
    return render(request, 'home.html',{'projects':pr})

def projects(request):
    if request.method == 'POST':
        alldata=request.POST
        projectname = alldata.get("projectname")
        projectcost = alldata.get("projectcost")
        p=Project(name=projectname,price_per_hour=projectcost)
        p.save()
    return render(request, 'projects.html')

def start_task(task):
    task.started = True
    task.start()

def stop_task(task):
    task.started = False
    task.stop()

def stop_fast_task(task,alldata):
    task.name = alldata.get("taskName")
    task.description = alldata.get("taskDescription")
    task.project= search_existing_project(alldata.get("newProjectName"))
    stop_task(task)


def first_div(task,action):
    if action == "Start" and task.started == False:
        start_task(task)
    if action == "Stop" and task.started == True:
        stop_task(task)

def start_second_div(user):
    task=Task(user=user,name="in_progress",started=True)
    task.save()
    task.start()
    return task,""

def search_existing_project(name_project):
    if Project.objects.filter(name=name_project):
        return Project.objects.filter(name=name_project)[0]
    else:
        np  = Project(name=name_project,price_per_hour=0)
        np.save()
        return np

def stop_second_div(user,alldata):
    task=Task.objects.get(user=user,name="in_progress")
    if alldata["newProjectName"] and alldata["taskName"]:
        stop_fast_task(task,alldata)
        return None, ""
    else:
        msg="You have left a empty field"
        task.started = True
        task.save()
        return task,msg

def second_div(action,alldata):
    if action == "Start":
        return start_second_div(UserProfile.objects.all()[0])
    if action == "Stop":
        return stop_second_div(UserProfile.objects.all()[0],alldata)

def yourtasks(request):
    if request.method == 'POST':
        alldata=request.POST           
        first_div(Task.objects.get(id=alldata.get("task_selected")),alldata.get("choisebuttom"))
    tasks=UserProfile.objects.all()[0].task_set.all().order_by('project__name')
    return render(request, 'yourtasks.html',{'tasks':tasks,'last_task':None,'message':''})

def fast_task(request):
    last_task=None
    msg=""
    if request.method == 'POST':
        tupla = second_div(request.POST.get("choisebuttom"),request.POST)
        last_task = tupla[0]
        msg = tupla[1]
    tasks=UserProfile.objects.all()[0].task_set.all().order_by('project__name')
    return render(request, 'yourtasks.html',{'tasks':tasks,'last_task':last_task,'message':msg})
