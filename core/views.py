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
        print "ES UN POSSSSSSSSSSST"
        alldata=request.POST
        taskname = alldata.get("taskname")
        taskdescription = alldata.get("taskdescription")
        projectname= alldata.get("projectname")
        p=Project.objects.get(name=projectname)
        print p
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

def yourtasks(request):
    c=UserProfile.objects.all()[0]
    p=Project.objects.all()[0]
    pr=Project.objects.all()
    last_task=None
    if request.method == 'POST':
        alldata=request.POST
        form=alldata.get("form_selected")
        if form =='form1':
            select_task= alldata.get("task_selected")
            action = alldata.get("choisebuttom")
            t = Task.objects.get(id=select_task)
            print t.name
            if action == "Start":
                t.started=True
                t.start()
            if action == "Stop":
                t.started=False
                t.stop()
            t.save()
        if form =='form2':
            action = alldata.get("choisebuttom")
            if action == "Start":
                tk=Task(user=c,name="in_progress")
                tk.save()
                tk.started=True
                tk.project=p
                tk.start()
                tk.save()
                last_task=tk

            if action == "Stop":
                tk=Task.objects.get(name="in_progress")
                tk.started = False
                tk.stop()
                tk.name = alldata.get("taskName")
                projectname= alldata.get("projectName")
                tk.project=Project.objects.get(name=projectname) 
                tk.save()

    tasks=c.task_set.all()
    return render(request, 'yourtasks.html',{'tasks':tasks,'last_task':last_task,'projects':pr}) 