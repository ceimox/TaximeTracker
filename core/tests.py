"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, RequestFactory
from core.models import UserProfile, Project, Task, Timer
from views import home, projects, yourtasks


class ProjectTest(TestCase):

    def test_al_hacer_post_se_crea_un_proyecreto(self):
        factory = RequestFactory()
        request = factory.post("/projects")
        request.POST["projectname"] = "project1"
        request.POST["projectcost"] = 2000 
        projects(request)
        projects_number = Project.objects.all().count()
        self.assertEqual(projects_number, 1)

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
        yourtasks(request)
        self.assertEqual(user.username,"si")    