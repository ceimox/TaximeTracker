"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, RequestFactory
from core.models import UserProfile, Project, Task, Timer
from views import home, projects, yourtasks, testview


class SimpleTest(TestCase):

    def test_al_abrir_home_retorna_200(self):
        factory = RequestFactory()
        request = factory.get("/projects")
        self.assertEqual(projects(request).status_code, 200)
