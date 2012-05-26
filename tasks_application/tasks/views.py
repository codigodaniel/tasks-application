from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Task
from models import Project
from forms import InboxForm
from forms import TaskForm
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

def global_data(request):
    r={}
    if request.user.is_authenticated():
        r['project_list']=Project.objects.filter(owner=request.user)
    else:
        r['project_list']=[]

    r['pending_list']=[]
    r['current_project']=request.session.get('current_project')
    active_tasks=Task.objects.filter(is_archived=False, is_blocked=False, is_delayed=False)
    
    bloqued_tasks=Task.objects.filter(is_blocked=True)
    delayed_tasks=Task.objects.filter(is_delayed=True)
    
    r['pending_list'].append({'label':'- de 5 min','list':active_tasks.filter(size=1)})
    r['pending_list'].append({'label':'+ de 5 min','list':active_tasks.filter(size=2)})
    r['pending_list'].append({'label':'+ de 2 horas','list':active_tasks.filter(size=3)})
    r['pending_list'].append({'label':'?','list':active_tasks.filter(size=4)})
    
    for qs in r['pending_list']:
        qs['list']=qs['list'].filter(project=r['current_project'])
    bloqued_tasks=bloqued_tasks.filter(project=r['current_project'])
    delayed_tasks=delayed_tasks.filter(project=r['current_project'])

    r['inbox_list']=active_tasks.filter(size=0)
    r['bloqued_tasks']=bloqued_tasks
    r['delayed_tasks']=delayed_tasks
    
    return r

def index(request):
    r=global_data(request)
    r['form']=InboxForm()
    return render_to_response('tasks/home.html', r, RequestContext(request))

def project_set(request, object_id):
    try:
        request.session['current_project']=Project.objects.get(pk=object_id)
    except:
        request.session['current_project']=None
        pass
    return HttpResponseRedirect(reverse('tasks_home'))
    
def process(request):
    r=global_data(request)
    inbox_first=None
    if r['inbox_list']:
        inbox_first=r['inbox_list'][0]
    r['form']=TaskForm(instance=inbox_first)
    r['inbox_first']=inbox_first
    return render_to_response('tasks/process.html', r, RequestContext(request))

def task_delay(request, object_id):
    try:
        obj=Task.objects.get(pk=object_id)
        if obj.is_delayed:
            obj.is_delayed=False
        else:
            obj.is_delayed=True 
        obj.save()
    except:
        pass
    return HttpResponseRedirect(reverse('tasks_home'))
    
def task_archive(request, object_id):
    try:
        obj=Task.objects.get(pk=object_id)
        obj.is_archived=True
        obj.save()
    except:
        pass
    return HttpResponseRedirect(reverse('tasks_home'))

def task_block(request, object_id):
    try:
        obj=Task.objects.get(pk=object_id)
        if obj.is_blocked:
            obj.is_blocked=False
        else:
            obj.is_blocked=True 
        obj.save()
    except:
        pass
    return HttpResponseRedirect(reverse('tasks_home'))
