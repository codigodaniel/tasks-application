from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from tasks.forms import InboxForm, TaskForm
from tasks.models import Project
from tasks.models import Task

from django.conf import settings

urlpatterns = patterns('',
    (r'^tasks/project/open/(?P<object_id>\d+)/$','tasks.views.project_set',{},'tasks_project_set'),

    (r'^tasks/task/(?P<object_id>\d+)/archive/$','tasks.views.task_archive',{},'tasks_task_archive'),

    (r'^tasks/task/(?P<object_id>\d+)/delay/$','tasks.views.task_delay',{},'tasks_task_delay'),

    #~ (r'^/accounts/login/','tasks.views.login_view',{}),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',{},'accounts_login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout',{},'accounts_logout'),
    
    #~ (r'^/accounts/logout/$','tasks.views.logout_view',{}),

    (r'^$','tasks.views.index',{},'tasks_home'),
    (r'^process/$','tasks.views.process',{},'tasks_process'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^tasks/project/new/$','django.views.generic.create_update.create_object',{'model':Project,'post_save_redirect':settings.HOME_URL},'tasks_project_new'),
    (r'^tasks/task/(?P<object_id>\d+)/edit/$','django.views.generic.create_update.update_object',{'form_class':TaskForm,'post_save_redirect':settings.HOME_URL},'tasks_task_edit'),
    (r'^tasks/task/(?P<object_id>\d+)/delete/$','django.views.generic.create_update.delete_object',{'model':Task,'post_delete_redirect':settings.HOME_URL},'tasks_task_delete'),
    (r'^inbox/insert/$','django.views.generic.create_update.create_object',{'form_class':InboxForm,'post_save_redirect':settings.HOME_URL},'tasks_inbox_insert'),
    (r'^process/update/(?P<object_id>\d+)/$','django.views.generic.create_update.update_object',{'form_class':TaskForm,'post_save_redirect':settings.HOME_URL+'process/'},'tasks_process_update'),
)

 
