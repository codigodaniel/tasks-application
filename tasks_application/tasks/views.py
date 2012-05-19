from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Task
from forms import InboxForm
from forms import TaskForm

def index(request):
    r={}
    r['form']=InboxForm()
    r['pending_list']=Task.objects.filter(size__gt=0, is_archived=False, is_closed=False).order_by('size')
    return render_to_response('tasks/home.html', r, RequestContext(request))

def process(request):
    r={}
    inbox_first=None
    r['inbox_list']=Task.objects.filter(size=0, is_archived=False, is_closed=False, is_blocked=False)
    if r['inbox_list']:
        inbox_first=r['inbox_list'][0]
    
    r['form']=TaskForm(instance=inbox_first)
    r['inbox_first']=inbox_first
    return render_to_response('tasks/process.html', r, RequestContext(request))
