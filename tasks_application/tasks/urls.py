from django.conf.urls.defaults import patterns, include, url

from tasks.forms import InboxForm, TaskForm, ProjectForm
from tasks.models import Project
from tasks.models import Task

from django.views.generic.simple import direct_to_template

from django.conf import settings

urlpatterns = patterns('tasks.views',
    (r'^project/open/(?P<object_id>\d+)/$','project_set',{},'tasks_project_set'),
    (r'^project/$','project_general',{},'tasks_project_general'),
    (r'^project/new/$','create_user_owned_object',{'model':Project,'form_class':ProjectForm,'post_save_redirect':settings.HOME_URL},'tasks_project_new'),
    (r'^project/(?P<object_id>\d+)/close/$','project_close',{},'tasks_project_close'),
    
    (r'^task/(?P<object_id>\d+)/edit/$','update_task',{'form_class':TaskForm,'post_save_redirect':settings.HOME_URL},'tasks_task_edit'),
    (r'^task/(?P<object_id>\d+)/block/$','task_block',{},'tasks_task_block'),
    (r'^task/(?P<object_id>\d+)/archive/$','task_archive',{},'tasks_task_archive'),
    (r'^task/(?P<object_id>\d+)/delay/$','task_delay',{},'tasks_task_delay'),
    (r'^task/(?P<object_id>\d+)/duplicate/$','task_duplicate',{},'tasks_task_duplicate'),
    (r'^task/(?P<object_id>\d+)/highlight/$','task_highlight',{},'tasks_task_highlight'),
    (r'^task/(?P<object_id>\d+)/detail/$','task_detail',{},'tasks_task_detail'),

    (r'^process/update/(?P<object_id>\d+)/$','update_task',{'form_class':TaskForm,'post_save_redirect':settings.HOME_URL+'tasks/process/'},'tasks_process_update'),
   
    (r'^inbox/insert/$','task_create',{'form_class':InboxForm,'post_save_redirect':settings.HOME_URL},'tasks_inbox_insert'),
   
    (r'^process/$','process',{},'tasks_process'),
    #~ (r'^archive/$','task_archived',{},'tasks_archived'),
    
    (r'^project/json/','project_json',{},'tasks_project_json'),
    (r'^task/json/','task_json',{},'tasks_task_json'),
)

urlpatterns += patterns('django.views.generic',
    (r'^project/(?P<object_id>\d+)/delete/$','create_update.delete_object',{'model':Project,'post_delete_redirect':settings.HOME_URL},'tasks_project_delete'),
    (r'^project/(?P<object_id>\d+)/edit/$','create_update.update_object',{'form_class':ProjectForm,'post_save_redirect':settings.HOME_URL},'tasks_project_edit'),
    
    #~ (r'^process/update/(?P<object_id>\d+)/$','create_update.update_object',{'form_class':TaskForm,'post_save_redirect':settings.HOME_URL+'tasks/process/'},'tasks_process_update'),
    #~ (r'^task/(?P<object_id>\d+)/edit/$','create_update.update_object',{'form_class':TaskForm,'post_save_redirect':settings.HOME_URL},'tasks_task_edit'),
    #~ (r'^tasks/project/new/$','create_update.create_object',{'model':Project,'post_save_redirect':settings.HOME_URL},'tasks_project_new'),
    (r'^task/(?P<object_id>\d+)/delete/$','create_update.delete_object',{'model':Task,'post_delete_redirect':settings.HOME_URL},'tasks_task_delete'),
    #~ (r'^inbox/insert/$','create_update.create_object',{'form_class':InboxForm,'post_save_redirect':settings.HOME_URL},'tasks_inbox_insert'),
    ('^archive/$', 'simple.direct_to_template', {'template': 'tasks/task_archived.html'},'tasks_archived'),
)
