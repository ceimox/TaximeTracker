from django.contrib import admin
from models import UserProfile, Project, Task, Timer

admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Timer)
admin.site.register(Task)