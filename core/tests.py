from django.test import TestCase, RequestFactory
from core.models import Project, Task, Timer
from views import home, projects, yourtasks
from core.models import start_task, stop_task, stop_fast_task, first_div
from core.models import stop_second_div, second_div, start_second_div
from core.models import search_existing_project
import datetime

class StartTaskTest(TestCase):

    def test_iniciar_tarea_para_cambiarle_el_estado_y_asignarle_un_timer(self):
        user = UserProfile(username="cesar", password="1234")
        user.save()
        t = Task(name="tarea1", user=user)
        t.save()
        start_task(t)
        tasks_started = Task.objects.filter(started=True).count() 
        self.assertEqual(tasks_started,1)
        temporal_timer = t.current_timer
        self.assertEqual(temporal_timer, Timer.objects.all()[0])
        timers = Timer.objects.all().count()
        self.assertEqual(timers,1)

class StopTaskTest(TestCase):
    def test_detener_tarea_para_cambiarle_el_estado_y_liberar_su_timer_temporal(self):
        user = UserProfile(username="cesar", password="1234")
        user.save()
        t = Task(name="tarea1", user=user)
        t.save()
        start_task(t)
        stop_task(t)
        tasks_stopped = Task.objects.filter(started=False).count() 
        self.assertEqual(tasks_stopped,1)
        temporal_timer = t.current_timer
        self.assertEqual(temporal_timer, None)
        timers = Timer.objects.all().count()
        self.assertEqual(timers,1)

class ProjectTest(TestCase):

    def test_al_hacer_post_se_crea_un_proyecto(self):
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
    
    def test_iniciar_una_tarea_para_crearle_un_cronometro_temporal_y_darle_su_tiempo_de_inicio(self):
        from datetime import timedelta
        user= UserProfile(username="cesar",password="1234",id=1)
        user.save()
        t1=Task(name="Task1",user=user)
        t1.save()
        t1.current_timer = Timer(task=t1)
        t1.current_timer.initial_time=datetime.datetime(2013, 10, 31, 17, 56, 1, 0)
        t1.current_timer.save()
        t1.save()
        timers= t1.timer_set.all().count()
        time=t1.current_timer
        self.assertEqual(timers,1)
        self.assertEqual(time.initial_time.second,1)

    def test_pausar_una_tarea_para_desvicularle_el_cronometro_temporal_y_asignarle_tiempo_final(self):
        from datetime import timedelta
        user= UserProfile(username="cesar",password="1234",id=1)
        user.save()
        t1=Task(name="Task1",user=user)
        t1.save()
        t1.current_timer = Timer(task=t1)
        t1.current_timer.final_time=datetime.datetime(2013, 10, 31, 17, 56, 1, 0)
        t1.current_timer.save()
        time=t1.current_timer
        self.assertEqual(time.final_time.second,1)
        t1.current_timer=None
        t1.save()
        timer_in_task = t1.current_timer
        self.assertEqual(timer_in_task,None)
        timers= t1.timer_set.all().count()
        self.assertEqual(timers,1)        

    def test_calcular_tiempo_para_devolver_el_tiempo_total_de_una_tarea(self):
        from datetime import timedelta
        user= UserProfile(username="cesar",password="1234",id=1)
        user.save()
        t1=Task(name="Task1",user=user)
        t1.save()
        t1.current_timer = Timer(task=t1)
        t1.current_timer.save()
        t1.current_timer.initial_time = datetime.datetime(2013, 10, 31, 17, 56, 1, 0)
        t1.current_timer.final_time = datetime.datetime(2013, 10, 31, 18, 56, 1, 0)
        t1.current_timer.save()
        t1.current_timer=None
        t1.current_timer = Timer(task=t1)
        t1.current_timer.save()
        t1.current_timer.initial_time = datetime.datetime(2013, 10, 31, 18, 56, 1, 0)
        t1.current_timer.final_time = datetime.datetime(2013, 10, 31, 19, 56, 1, 0)
        t1.current_timer.save()
        result = t1.calculate_time()
        self.assertEqual(result,2)

    def test_calcular_costo_para_obtener_el_valor_total_por_una_tarea_con_todos_sus_tiempos(self):
        user= UserProfile(username="cesar",password="1234")
        user.save()
        project=Project(name="test_project",price_per_hour=4000)
        project.save()
        t1=Task(name="Task1",user=user,project=project)
        t1.save()
        t1.current_timer = Timer(task=t1)
        t1.current_timer.save()
        t1.current_timer.initial_time = datetime.datetime(2013, 10, 31, 17, 56, 1, 0)
        t1.current_timer.final_time = datetime.datetime(2013, 10, 31, 18, 56, 1, 0)
        t1.current_timer.save()
        t1.current_timer=None
        t1.current_timer = Timer(task=t1)
        t1.current_timer.save()
        t1.current_timer.initial_time = datetime.datetime(2013, 10, 31, 18, 56, 1, 0)
        t1.current_timer.final_time = datetime.datetime(2013, 10, 31, 19, 56, 1, 0)
        t1.current_timer.save()
        result = t1.calculate_cost()
        self.assertEqual(result,8000)
