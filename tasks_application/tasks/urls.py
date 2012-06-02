from django.conf.urls.defaults import patterns, include, url

from tasks.forms import InboxForm, TaskForm, ProjectForm
from tasks.models import Project
from tasks.models import Task

from django.conf import settings

urlpatterns = patterns('tasks.views',
    (r'^project/open/(?P<object_id>\d+)/$','project_set',{},'tasks_project_set'),
    (r'^project/new/$','create_user_owned_object',{'model':Project,'form_class':ProjectForm,'post_save_redirect':settings.HOME_URL},'tasks_project_new'),
    
    (r'^task/(?P<object_id>\d+)/edit/$','save_or_continue_editing',{'form_class':TaskForm,'post_save_redirect':settings.HOME_URL},'tasks_task_edit'),
    (r'^task/(?P<object_id>\d+)/block/$','task_block',{},'tasks_task_block'),
    (r'^task/(?P<object_id>\d+)/archive/$','task_archive',{},'tasks_task_archive'),
    (r'^task/(?P<object_id>\d+)/delay/$','task_delay',{},'tasks_task_delay'),
    (r'^process/$','process',{},'tasks_process'),
    (r'^archive/$','task_archived',{},'tasks_archived'),
)

urlpatterns += patterns('django.views.generic',
    (r'^process/update/(?P<object_id>\d+)/$','create_update.update_object',{'form_class':TaskForm,'post_save_redirect':settings.HOME_URL+'process/'},'tasks_process_update'),
    #~ (r'^tasks/project/new/$','create_update.create_object',{'model':Project,'post_save_redirect':settings.HOME_URL},'tasks_project_new'),
    #~ (r'^task/(?P<object_id>\d+)/edit/$','create_update.update_object',{'form_class':TaskForm,'post_save_redirect':settings.HOME_URL},'tasks_task_edit'),
    (r'^task/(?P<object_id>\d+)/delete/$','create_update.delete_object',{'model':Task,'post_delete_redirect':settings.HOME_URL},'tasks_task_delete'),
    (r'^inbox/insert/$','create_update.create_object',{'form_class':InboxForm,'post_save_redirect':settings.HOME_URL},'tasks_inbox_insert'),
)

