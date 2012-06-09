from models import Task
from models import Project
from forms import InboxForm

def tasks_dicts(request):
    r={}
    if request.user.is_authenticated():
        r['project_list']=Project.objects.filter(owner=request.user).filter(is_closed=False)
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
    
    if r['current_project']:
        for qs in r['pending_list']:
            qs['list']=qs['list'].filter(project=r['current_project'])
        bloqued_tasks=bloqued_tasks.filter(project=r['current_project'])
        delayed_tasks=delayed_tasks.filter(project=r['current_project'])
    else:
        for qs in r['pending_list']:
            qs['list']=qs['list'].filter(project__in=r['project_list'])
        bloqued_tasks=bloqued_tasks.filter(project__in=r['project_list'])
        delayed_tasks=delayed_tasks.filter(project__in=r['project_list'])

    r['inbox_list']=active_tasks.filter(size=0)
    r['bloqued_tasks']=bloqued_tasks
    r['delayed_tasks']=delayed_tasks
    
    r['inbox_form']=InboxForm()
    
    return r
    
