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
    pr=Project.objects.all()
    last_task=None
    msg=""
    if request.method == 'POST':
        alldata=request.POST
        form=alldata.get("form_selected")
        if form =='form1':
            select_task= alldata.get("task_selected")
            action = alldata.get("choisebuttom")
            t = Task.objects.get(id=select_task)
            if action == "Start" and t.started == False:
                t.started=True
                t.start()
            if action == "Stop" and t.started == True:
                t.started=False
                t.stop()
            t.save()
        if form =='form2':
            action = alldata.get("choisebuttom")
            if action == "Start":
                tk=Task(user=c,name="in_progress")
                tk.save()
                tk.started=True
                tk.start()
                tk.save()
                last_task=tk

            if action == "Stop":
                tk=Task.objects.get(user=c,name="in_progress")
                if request.POST["newProjectName"] and request.POST["pricePerHour"] and request.POST["taskName"]:
                    tk.name = alldata.get("taskName")
                    tk.description = alldata.get("taskDescription")
                    projectNameme = alldata.get("newProjectName")
                    project_price_per_hour = alldata.get("pricePerHour")
                    np  = Project(name=projectname,price_per_hour=project_price_per_hour)
                    np.save()
                    tk.project= np
                    tk.started = False
                    tk.stop()
                    tk.save()              
                elif (request.POST["newProjectName"] == "" and request.POST["pricePerHour"]) or (request.POST["newProjectName"] and request.POST["pricePerHour"]== "") or request.POST["taskName"]== "":
                    msg="You have left a empty field"
                    tk.started = True
                    last_task = tk
                    tk.save()
                elif request.POST["newProjectName"] =="" and request.POST["pricePerHour"] == "":
                    tk.stop()
                    tk.name = alldata.get("taskName")
                    tk.description = alldata.get("taskDescription")
                    projectname= alldata.get("projectName")
                    tk.project=Project.objects.get(name=projectname)
                    tk.started = False
                    tk.save()

    tasks=c.task_set.all()
    return render(request, 'yourtasks.html',{'tasks':tasks,'last_task':last_task,'projects':pr,'message':msg}) 