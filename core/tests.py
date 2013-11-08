"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, RequestFactory
from core.models import UserProfile, Project, Task, Timer
from views import home, projects, yourtasks
import datetime


class ProjectTest(TestCase):

    def test_al_hacer_post_se_crea_un_proyecreto(self):
        factory = RequestFactory()
        request = factory.post("/projects")
        request.POST["projectname"] = "project1"
        request.POST["projectcost"] = 2000 
        projects(request)
        projects_number = Project.objects.all().count()
        self.assertEqual(projects_number, 1)

class HomeTest(TestCase):

    def test_al_hacer_post_se_crea_una_tarea(self):
        user= UserProfile(username="cesar",password="1234",id=1)
        user.save()
        p=Project(name="testProject",price_per_hour=4000)
        p.save()
        factory = RequestFactory()
        request = factory.post("/home")
        request.POST["projectname"] = "testProject"
        request.POST["taskname"] = "testTask"
        result = home(request)
        projects_number = Project.objects.all().count()
        tasks_number = Task.objects.all().count()
        self.assertEqual(projects_number, 1)
        self.assertEqual(tasks_number, 1)

class YourtaskTest(TestCase):

    def test_al_entrar_en_form1_y_iniciar_tarea(self):
        user= UserProfile(username="cesar",password="1234",id=1)
        user.save()
        factory = RequestFactory()
        request = factory.post("/yourtasks")
        t=Task(name="tarea1",user=user)
        t.save()
        request.POST["form_selected"] = "form1"
        request.POST["task_selected"] = t.id
        request.POST["choisebuttom"] = "Start"
        result = yourtasks(request)
        tasks_started = Task.objects.filter(started=True).count() 
        self.assertEqual(tasks_started,1)

    def test_al_entrar_en_form1_y_detener_tarea(self):
        user= UserProfile(username="cesar",password="1234",id=1)
        user.save()
        factory = RequestFactory()
        request = factory.post("/yourtasks")
        p = Project(name="testProject",price_per_hour=4000)
        p.save()
        t = Task(name="tarea1", user=user, started=True, project=p)
        t.save()
        t.start()
        t.save()
        request.POST["form_selected"] = "form1"
        request.POST["task_selected"] = t.id
        request.POST["choisebuttom"] = "Stop"
        result = yourtasks(request)
        tasks_stopped = Task.objects.filter(started=False).count() 
        self.assertEqual(tasks_stopped,1)
        
    def test_al_entrar_en_form2_y_iniciar_tarea(self):
        user= UserProfile(username="cesar",password="1234",id=1)
        user.save()
        factory = RequestFactory()
        request = factory.post("/yourtasks")
        request.POST["form_selected"] = "form2"
        request.POST["choisebuttom"] = "Start"
        result = yourtasks(request)
        tasks_started = Task.objects.filter(started=True).count() 
        self.assertEqual(tasks_started,1)

    def test_al_entrar_en_form2_y_finalizar_tarea_con_ningun_campo_vacio(self):
        user= UserProfile(username="cesar",password="1234",id=1)
        user.save()
        tk=Task(user=user,name="in_progress")
        tk.save()
        tk.started=True
        tk.start()
        tk.save()
        factory = RequestFactory()
        request = factory.post("/yourtasks")
        request.POST["form_selected"] = "form2"
        request.POST["taskName"] = "TestTask"
        request.POST["newProjectName"] = "Project1"
        request.POST["pricePerHour"] = 4000
        request.POST["choisebuttom"] = "Stop"
        result = yourtasks(request)
        tasks_stopped = Task.objects.filter(started=False).count() 
        projects_number = Project.objects.all().count()
        self.assertEqual(tasks_stopped+projects_number,2)

    def test_al_entrar_en_form2_y_finalizar_tarea_con_campo_de_tarea_vacio(self):
        user= UserProfile(username="cesar",password="1234",id=1)
        user.save()
        tk=Task(user=user,name="in_progress")
        tk.save()
        tk.started=True
        tk.start()
        tk.save()
        factory = RequestFactory()
        request = factory.post("/yourtasks")
        request.POST["form_selected"] = "form2"
        request.POST["taskName"] = ""
        request.POST["newProjectName"] = "Project1"
        request.POST["pricePerHour"] = 4000
        request.POST["choisebuttom"] = "Stop"
        result = yourtasks(request)
        tasks_stopped = Task.objects.filter(started=False).count() 
        projects_number = Project.objects.all().count()
        self.assertEqual(tasks_stopped+projects_number,0)

    def test_al_entrar_en_form2_y_finalizar_tarea_con_campo_de_nombre_de_proyecto_vacio(self):
        user= UserProfile(username="cesar",password="1234",id=1)
        user.save()
        tk=Task(user=user,name="in_progress")
        tk.save()
        tk.started=True
        tk.start()
        tk.save()
        factory = RequestFactory()
        request = factory.post("/yourtasks")
        request.POST["form_selected"] = "form2"
        request.POST["taskName"] = "TestTask"
        request.POST["newProjectName"] = ""
        request.POST["pricePerHour"] = 4000
        request.POST["choisebuttom"] = "Stop"
        result = yourtasks(request)
        tasks_stopped = Task.objects.filter(started=False).count() 
        projects_number = Project.objects.all().count()
        self.assertEqual(tasks_stopped+projects_number,0)

    def test_al_entrar_en_form2_y_finalizar_tarea_con_campo_de_precio_de_proyecto_vacio(self):
        user= UserProfile(username="cesar",password="1234",id=1)
        user.save()
        tk=Task(user=user,name="in_progress")
        tk.save()
        tk.started=True
        tk.start()
        tk.save()
        factory = RequestFactory()
        request = factory.post("/yourtasks")
        request.POST["form_selected"] = "form2"
        request.POST["taskName"] = "TestTask"
        request.POST["newProjectName"] = "Project1"
        request.POST["pricePerHour"] = None
        request.POST["choisebuttom"] = "Stop"
        result = yourtasks(request)
        tasks_stopped = Task.objects.filter(started=False).count() 
        projects_number = Project.objects.all().count()
        self.assertEqual(tasks_stopped+projects_number,0)

    def test_al_entrar_en_form2_y_finalizar_tarea_con_campo_de_nombre_de_tarea_lleno_y_con_campos_de_proyecto_vacios(self):
        user= UserProfile(username="cesar",password="1234",id=1)
        user.save()
        tk=Task(user=user,name="in_progress")
        tk.save()
        tk.started=True
        tk.start()
        tk.save()
        p=Project(name="testProject",price_per_hour=4000)
        p.save()
        factory = RequestFactory()
        request = factory.post("/yourtasks")
        request.POST["form_selected"] = "form2"
        request.POST["taskName"] = "TestTask"
        request.POST["newProjectName"] = None
        request.POST["projectName"] = "testProject"
        request.POST["pricePerHour"] = None
        request.POST["choisebuttom"] = "Stop"
        result = yourtasks(request)
        tasks_started = Task.objects.filter(started=True).count() 
        projects_number = Project.objects.all().count()
        self.assertEqual(tasks_started+projects_number,2)

class TaskTest(TestCase):
    def test_calcular_tiempo_para_devolver_el_tiempo_total_de_todas_las_tareas(self):
        user= UserProfile(username="cesar",password="1234",id=1)
        user.save()
        t1=Task(name="Task1",user=user)
        t2=Task(name="Task2",user=user)
        t1.save()
        t2.save()
        t1.current_timer = Timer(task=self)
        timedelta1 = (2013, 10, 31, 17, 55, 1, 793006)
        timedelta2 = (2013, 10, 31, 17, 56, 1, 660723)
        t1.current_timer.initial_time = timedelta
        