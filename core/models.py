from django.db import models
from django.contrib.auth.models import User
import datetime


def calculate_total_cost(user) :
    tasks = user.task_set.all()
    total = sum([current.calculate_cost() for current in tasks])
    return total

class Project(models.Model):
    name = models.CharField(primary_key=True, max_length=200)
    price_per_hour = models.IntegerField()

    def __unicode__(self):
        return  self.name

    def calculate_cost(self):
        tasks = self.task_set.all()
        total = sum([current.calculate_cost() for current in tasks])
        return total

class Task(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(max_length=200, null=True)
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project, null=True)
    started = models.BooleanField()

    def __unicode__(self):
        return u'%s %s' % (self.name,self.description)

    def start(self):
        self.current_timer = Timer(task=self)
        self.current_timer.initial_time = datetime.datetime.now()
        self.current_timer.save()
        self.save()

    def stop(self):
        self.current_timer = Timer.objects.get(task=self, final_time=None)
        self.current_timer.final_time=datetime.datetime.now()
        self.current_timer.save()
        self.current_timer = None
        self.save()

    def calculate_time(self) :
        timers = self.timer_set.all()
        total = sum([current.total_time for current in timers])
        return float(total) / float(3600)

    def time_formated(self):
        from datetime import timedelta
        delta = timedelta(hours = self.calculate_time())
        return "%02d:%02d" % (delta.seconds // 3600, delta.seconds // 60 % 60)


    def calculate_cost(self):
        hours = self.calculate_time()
        if self.project:
            current_cost = int(hours * int(self.project.price_per_hour))
        else:
            current_cost = 0
        return current_cost

class Timer(models.Model):
    initial_time = models.DateTimeField(null=True)
    final_time = models.DateTimeField(null=True)
    task = models.ForeignKey(Task, null=True)

    @property
    def total_time(self):
        timedelta = self.final_time-self.initial_time
        return timedelta.seconds

def start_task(task):
    task.started = True
    task.start()

def stop_task(task):
    task.started = False
    task.stop()

def stop_fast_task(task, alldata):
    task.name = alldata.get("taskName")
    task.description = alldata.get("taskDescription")
    task.project = search_existing_project(alldata.get("newProjectName"))
    stop_task(task)

def first_div(task, action):
    if action == "Start" and task.started == False:
        start_task(task)
    if action == "Stop" and task.started == True:
        stop_task(task)

def start_second_div(user):
    task = Task.objects.create(user = user, name = "in_progress", started = True)
    task.start()
    return task, ""

def search_existing_project(name_project):
    if Project.objects.filter(name = name_project):
        return Project.objects.filter(name = name_project)[0]
    else:
        np = Project.objects.create(name = name_project, price_per_hour = 0)
        return np

def stop_second_div(user, alldata):
    task = Task.objects.get(user = user, name = "in_progress")
    if alldata["newProjectName"] and alldata["taskName"]:
        stop_fast_task(task, alldata)
        return None, ""
    else:
        msg = "You have left a empty field"
        task.started = True
        task.save()
        return task, msg

def second_div(action, alldata, user):
    if action == "Start":
        return start_second_div(user)
    if action == "Stop":
        return stop_second_div(user, alldata)