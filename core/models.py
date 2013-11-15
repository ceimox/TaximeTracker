from django.db import models
from django.contrib.auth.models import User
import datetime

class UserProfile(User):
    
    def __unicode__(self):
        return  self.username

    def start_task(self):
        self.task = Task(user=self)
        name_task=raw_input("put the task name\n")
        self.task.name=name_task
        description_task=raw_input("put the task description\n")
        self.task.description= description_task
        self.task.save()
        name_project= raw_input("put the project name\n")
        price_project= raw_input("put price per hour of the project\n")
        self.project= Project(name = name_project, price_per_hour = price_project)
        self.project.save()
        self.task.project= self.project
        self.task.start()
        self.task.save()
        d="0"
        while d!="2" :
            d=raw_input("press 1 to pause the task, 2 to finish: ")
            if d=="2":
                self.task.stop()
                self.task.save()
            if d=="1":
                self.task.stop()
                self.task.save()
                d2=raw_input("press 1 to reanude the task, 2 to finish: ")
                if d2=="1":
                    self.task.start()
                    self.task.save()
                if d2=="2":
                    d="2"

    def calculate_total_cost(self) :
        tasks=self.task_set.all()
        total=0
        for current in tasks:
            print "the current cost of the task ",current.name,"is: ", current.calculate_cost()
            total = current.calculate_cost() + total
        print "the total cost is :", total


class Project(models.Model):
    name = models.CharField(primary_key=True,max_length= 200)
    price_per_hour = models.IntegerField()
    
    def __unicode__(self):
        return  self.name
    
    def calculate_cost(self):
        tasks=self.task_set.all()
        total=0
        for current in tasks:
            print "the current cost of the task ",current.name,"is: ", current.calculate_cost()
            total = current.calculate_cost() + total
        print "the total cost is :", total


class Task(models.Model):
    name = models.CharField(max_length=200,null=True)
    description = models.TextField(max_length=200,null=True)
    user = models.ForeignKey(UserProfile)
    project = models.ForeignKey(Project,null=True)
    started = models.BooleanField()
   # current_timer=models.ForeignKey(Timer)
 
    def __unicode__(self):
        return u'%s %s' % (self.name,self.description)

    def start(self):
        self.current_timer = Timer(task=self)
        self.current_timer.initial_time=datetime.datetime.now()
        self.current_timer.save()
        self.save()
    
    def stop(self):
        self.current_timer = Timer.objects.get(task=self, final_time=None)
        self.current_timer.final_time=datetime.datetime.now()
        self.current_timer.save()
        self.current_timer= None
        self.save()
    
    def calculate_time(self) :
        timers=self.timer_set.all()
        total=0
        for current in timers:
            print current.total_time
            total = current.total_time + total
        print "the total is :", total

        return float(total)/float(3600)

    def time_formated(self):
        from datetime import timedelta
        delta = timedelta(hours=self.calculate_time())
        return "%02d:%02d" % (delta.seconds//3600, delta.seconds // 60 % 60)


    def calculate_cost(self):
        hours = self.calculate_time()
        if self.project:
            current_cost = int(hours*int(self.project.price_per_hour))
        else:
            current_cost=0
        return current_cost


class Timer(models.Model):
    initial_time = models.DateTimeField(null=True)
    final_time = models.DateTimeField(null=True)
    task = models.ForeignKey(Task,null=True)

    @property
    def total_time(self):
        timedelta = self.final_time-self.initial_time
        return timedelta.seconds


