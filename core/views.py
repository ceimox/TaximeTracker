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
    if request.method == 'GET':
        alldata=request.GET
        projectname = alldata.get("projectname")
        projectcost = alldata.get("projectcost")
        p=Project(name=projectname,price_per_hour=projectcost)
        p.save()
    return render(request, 'projects.html') 

def yourtasks(request):
    c=UserProfile.objects.all()[0]
    tasks=c.task_set.all()
    return render(request, 'yourtasks.html',{'tasks':tasks}) 
