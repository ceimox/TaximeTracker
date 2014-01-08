from django.db import models
from django.contrib.auth.models import User
from core.lib.time_delta import TimeDelta
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

    def calculate_time(self):
      total = 0
      for t in self.task_set.all():
        total += t.calculate_time()

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
        delta = TimeDelta(sum([current.total_time for current in timers]))
        return delta

    def time_formated(self):
        delta = self.calculate_time()
        return "%02d:%02d:%02d" % (delta.days, delta.hours, delta.minutes)


    def calculate_cost(self):
        hours = self.calculate_time().hours
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

def fast_task_stopped(task, alldata):
    task.name = alldata.get("taskName")
    task.description = alldata.get("taskDescription")
    task.project = search_existing_project(alldata.get("newProjectName"))
    stop_task(task)

def choise_action_yourtasks(task, action):
    if action == "Start" and task.started == False:
        start_task(task)
    if action == "Stop" and task.started == True:
        stop_task(task)

def start_fast_task(user):
    task = Task.objects.create(user = user, name = "in_progress", started = True)
    task.start()

def search_existing_project(name_project):
    if Project.objects.filter(name = name_project):
        return Project.objects.filter(name = name_project)[0]
    else:
        np = Project.objects.create(name = name_project, price_per_hour = 0)
        return np

def stop_fast_task(user, alldata):
    task = Task.objects.get(user = user, name = "in_progress")
    if alldata["newProjectName"] and alldata["taskName"]:
        fast_task_stopped(task, alldata)
    else:
        task.started = True
        task.save()

def choise_action_fast_task(action, alldata, user):
    if action == "Start":
        start_fast_task(user)
    if action == "Stop":
        stop_fast_task(user, alldata)

def search_task(request):
    if Task.objects.filter(name = "in_progress",user = req.user):
        return Task.objects.filter(name = "in_progress", user=req.user)
    else:
        return None