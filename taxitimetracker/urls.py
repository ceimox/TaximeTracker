from django.conf.urls import patterns, include, url
from core.views import fast_task, yourtasks, home, projects
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^home', home),
    url(r'^projects', projects),
    url(r'^yourtasks', yourtasks),
    url(r'^fasttask', fast_task),
    # url(r'^taxitimetracker/', include('taxitimetracker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
