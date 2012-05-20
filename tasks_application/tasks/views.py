from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Task
from models import Project
from forms import InboxForm
from forms import TaskForm

def global_data(request):
    r={}
    r['pending_list']=[]
    r['current_project']=request.session.get('current_project')
    active_tasks=Task.objects.filter(is_archived=False, is_closed=False)
    #~ r['pending_list']=Task.objects.filter(size__gt=0, is_archived=False, is_closed=False).order_by('size')
    
    r['pending_list'].append({'label':'- de 5 min','list':active_tasks.filter(size=1)})
    r['pending_list'].append({'label':'+ de 5 min','list':active_tasks.filter(size=2)})
    r['pending_list'].append({'label':'+ de 2 horas','list':active_tasks.filter(size=3)})
    r['pending_list'].append({'label':'?','list':active_tasks.filter(size=4)})
    
    project_to_filter=0
    if r['current_project']:
        project_to_filter=r['current_project']
    for qs in r['pending_list']:
        qs['list']=qs['list'].filter(project=r['current_project'])
    
    r['inbox_list']=active_tasks.filter(size=0, is_blocked=False)
    return r

def index(request):
    r=global_data(request)
    r['form']=InboxForm()
    r['project_list']=Project.objects.all()
    return render_to_response('tasks/home.html', r, RequestContext(request))

def project_set(request, object_id):
    try:
        request.session['current_project']=Project.objects.get(pk=object_id)
    except:
        request.session['current_project']=None
        pass
    return HttpResponseRedirect('/')
    
def process(request):
    r=global_data(request)
    inbox_first=None
    if r['inbox_list']:
        inbox_first=r['inbox_list'][0]
    r['form']=TaskForm(instance=inbox_first)
    r['inbox_first']=inbox_first
    return render_to_response('tasks/process.html', r, RequestContext(request))

