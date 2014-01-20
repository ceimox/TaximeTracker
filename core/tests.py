from django.test import TestCase, RequestFactory
from core.models import Project, Task, Timer
from django.contrib.auth.models import User
from views import home, projects, yourtasks, fast_task, your_task_current_month
from core.models import start_task, stop_task, stop_fast_task, choise_action_yourtasks
from core.models import stop_fast_task, choise_action_fast_task, start_fast_task
from core.models import search_existing_project
import datetime
from core.lib.time_delta import TimeDelta

class YourTaskTemplateTest(TestCase):

    def test_al_hacer_get_en_yourtask_se_obtienen_dos_enlaces_de_tareas_actuales_y_antiguas(self):
        user = User(username="cesar", password="1234")
        user.save()
        factory = RequestFactory()
        request = factory.get("/yourtasks")
        request.user = user
        result = yourtasks(request)
        self.assertIn('<a href="/yourtasks/current_month">Current month</a>',result.content)
        self.assertIn('<a href="/yourtasks/all_tasks">All Tasks</a>',result.content)
        self.assertEqual(result.status_code,200)

    def test_al_hacer_get_en_enlace_de_tareas_del_mes_actual_muestra_solo_esas_tareas(self):
        user = User(username="cesar", password="1234")
        user.save()

        project=Project(name="test_project",price_per_hour=4000)
        project.save()

        t1 = Task(name="tarea1", user=user, project=project)
        t1.save()
        t1.start()
        t1.stop()

        other_month = datetime.datetime.now() - datetime.timedelta(days=32)

        t2= Task(name="tarea2", user=user,project=project)
        t2.save()
        t2.current_timer = Timer(task=t2)
        t2.current_timer.initial_time = other_month
        t2.current_timer.save()
        t2.save()
        t2.stop()

        t3=Task(name="tarea3",user=user,project=project)
        t3.save()
        t3.current_timer = Timer(task=t3)
        t3.current_timer.initial_time = other_month
        t3.current_timer.save()
        t3.current_timer.final_time = other_month
        t3.current_timer.save()

        factory = RequestFactory()
        request = factory.get("/yourtasks/current_month")
        request.user = user
        result = your_task_current_month(request)
        self.assertIn(t1.name,result.content)
        self.assertIn(t2.name,result.content)
        self.assertNotIn(t3.name,result.content)
        self.assertEqual(result.status_code,200)


    def test_al_hacer_get_en_enlace_de_todas_las_tareas_muestra_esas_tareas(self):
        user = User(username="cesar", password="1234")
        user.save()

        project=Project(name="test_project",price_per_hour=4000)
        project.save()

        t1 = Task(name="tarea1", user=user, project=project)
        t1.save()
        t1.start()
        t1.stop()

        other_month = datetime.datetime.now() - datetime.timedelta(days=32)

        t2= Task(name="tarea2", user=user,project=project)
        t2.save()
        t2.current_timer = Timer(task=t2)
        t2.current_timer.initial_time = other_month
        t2.current_timer.save()
        t2.save()
        t2.stop()

        t3=Task(name="tarea3",user=user,project=project)
        t3.save()
        t3.current_timer = Timer(task=t3)
        t3.current_timer.initial_time = other_month
        t3.current_timer.save()
        t3.current_timer.final_time = other_month
        t3.current_timer.save()

        factory = RequestFactory()
        request = factory.get("/yourtasks")
        request.user = user
        result = yourtasks(request)
        self.assertIn(t1.name,result.content)
        self.assertIn(t2.name,result.content)
        self.assertIn(t3.name,result.content)
        self.assertEqual(result.status_code,200)



class TimeDeltaTest(TestCase):
    def test_seconds_deberia_retornar_86400_cuando_se_pasan_86400_segundos_al_constructor(self):
        delta = TimeDelta(86400)
        self.assertEqual(delta.seconds, 86400)

    def test_minutes_deberia_retornar_1400_cuando_se_pasan_86400_segundos_al_constructor(self):
        delta = TimeDelta(86400)
        self.assertEqual(delta.minutes, 1440)

    def test_hours_deberia_retornar_24_cuando_se_pasan_86400_segundos_al_constructor(self):
        delta = TimeDelta(86400)
        self.assertEqual(delta.hours, 24)

    def test_days_deberia_retornar_1_cuando_se_pasan_86400_segundos_al_constructor(self):
        delta = TimeDelta(86400)
        self.assertEqual(delta.days, 1)


class StartTaskTest(TestCase):

    def test_iniciar_tarea_para_cambiarle_el_estado_y_asignarle_un_timer(self):
        user = User(username="cesar", password="1234")
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
        user = User(username="cesar", password="1234")
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
        user= User(username="cesar",password="1234")
        user.save()
        p=Project(name="testProject",price_per_hour=4000)
        p.save()
        factory = RequestFactory()
        request = factory.post("/home")
        request.user = user
        request.POST["projectname"] = "testProject"
        request.POST["taskname"] = "testTask"
        result = home(request)
        projects_number = Project.objects.all().count()
        tasks_number = Task.objects.all().count()
        self.assertEqual(projects_number, 1)
        self.assertEqual(tasks_number, 1)


class YourtasksTest(TestCase):

    def test_al_hacer_post_para_inciar_una_tarea(self):
        user= User(username="cesar",password="1234")
        user.save()
        factory = RequestFactory()
        request = factory.post("/yourtasks")
        p = Project(name="testProject",price_per_hour=4000)
        p.save()
        t = Task(name="tarea1", user=user, started=True, project=p)
        t.save()
        request.user = user
        request.POST["task_selected"] = t.id
        request.POST["choisebuttom"] = "Start"
        result = yourtasks(request)
        tasks_started = Task.objects.filter(started=True).count()
        self.assertEqual(tasks_started,1)

    def test_al_hacer_post_para_detener_una_tarea(self):
        user= User(username="cesar",password="1234")
        user.save()
        factory = RequestFactory()
        request = factory.post("/yourtasks")
        p = Project(name="testProject",price_per_hour=4000)
        p.save()
        t = Task(name="tarea1", user=user, started=True, project=p)
        t.save()
        t.start()
        t.save()
        request.user = user
        request.POST["task_selected"] = t.id
        request.POST["choisebuttom"] = "Stop"
        result = yourtasks(request)
        tasks_stopped = Task.objects.filter(started=False).count()
        self.assertEqual(tasks_stopped,1)

class FastTaskTest(TestCase):

    def test_al_iniciar_tarea_para_iniciar_una_tarea(self):
        user= User(username="cesar",password="1234")
        user.save()
        factory = RequestFactory()
        request = factory.post("/fasttask")
        request.POST["choisebuttom"] = "Start"
        request.user = user
        result = fast_task(request)
        tasks_started = Task.objects.filter(started=True).count()
        self.assertEqual(tasks_started,1)

    def test_al_detener_tarea_con_ningun_campo_vacio_para_detener_tarea_y_crear_proyecto(self):
        user= User(username="cesar",password="1234")
        user.save()
        tk=Task(user=user,name="in_progress")
        tk.save()
        tk.started=True
        tk.start()
        tk.save()
        factory = RequestFactory()
        request = factory.post("/fasttask")
        request.user = user
        request.POST["taskName"] = "TestTask"
        request.POST["newProjectName"] = "Project1"
        request.POST["choisebuttom"] = "Stop"
        result = fast_task(request)
        tasks_stopped = Task.objects.filter(started=False).count()
        projects_number = Project.objects.all().count()
        self.assertEqual(tasks_stopped+projects_number,2)

    def test_al_detener_tarea_con_campo_de_tarea_vacio_para_no_detener_tarea_ni_crear_proyecto(self):
        user= User(username="cesar",password="1234")
        user.save()
        tk=Task(user=user,name="in_progress")
        tk.save()
        tk.started=True
        tk.start()
        tk.save()
        factory = RequestFactory()
        request = factory.post("/fasttask")
        request.user = user
        request.POST["taskName"] = ""
        request.POST["newProjectName"] = "Project1"
        request.POST["choisebuttom"] = "Stop"
        result = fast_task(request)
        tasks_stopped = Task.objects.filter(started=False).count()
        projects_number = Project.objects.all().count()
        self.assertEqual(tasks_stopped+projects_number,0)

    def test_al_detener_tarea_con_campo_de_proyecto_vacio_para_no_detener_tarea_ni_crear_proyecto(self):
        user= User(username="cesar",password="1234")
        user.save()
        tk=Task(user=user,name="in_progress")
        tk.save()
        tk.started=True
        tk.start()
        tk.save()
        factory = RequestFactory()
        request = factory.post("/fasttask")
        request.user = user
        request.POST["taskName"] = "TestTask"
        request.POST["newProjectName"] = ""
        request.POST["choisebuttom"] = "Stop"
        result = fast_task(request)
        tasks_stopped = Task.objects.filter(started=False).count()
        projects_number = Project.objects.all().count()
        self.assertEqual(tasks_stopped+projects_number,0)


class TaskTest(TestCase):

    def test_iniciar_una_tarea_para_crearle_un_cronometro_temporal_y_darle_su_tiempo_de_inicio(self):
        from datetime import timedelta
        user= User(username="cesar",password="1234")
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
        user= User(username="cesar",password="1234")
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
        user= User(username="cesar",password="1234")
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
        self.assertEqual(result.hours,2)

    def test_calcular_costo_para_obtener_el_valor_total_por_una_tarea_con_todos_sus_tiempos(self):
        user= User(username="cesar",password="1234")
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

    def test_current_month_tasks_deberia_retortar_solo_las_tareas_que_tienen_timers_en_el_mes_actual(self):
        from datetime import datetime, timedelta

        user = User(username="cesar",password="1234")
        user.save()

        project=Project(name="test_project",price_per_hour=4000)
        project.save()

        last_month = datetime.today() - timedelta(days=32)

        t1=Task(name="Task1",user=user,project=project)
        t1.save()
        t1.current_timer = Timer(task=t1)
        t1.current_timer.save()

        t1.current_timer.initial_time = last_month
        t1.current_timer.final_time = last_month
        t1.current_timer.save()

        t2=Task(name="Task2",user=user,project=project)
        t2.save()
        t2.current_timer = Timer(task=t2)
        t2.current_timer.save()

        t2.current_timer.initial_time = last_month
        t2.current_timer.final_time = datetime.today()
        t2.current_timer.save()

        t3=Task(name="Task3",user=user,project=project)
        t3.save()
        t3.current_timer = Timer(task=t3)
        t3.current_timer.save()

        t3.current_timer.initial_time = datetime.today()
        t3.current_timer.final_time = datetime.today()
        t3.current_timer.save()

        result = Task.objects.current_month_tasks()
        self.assertEqual(result, [t2, t3])
