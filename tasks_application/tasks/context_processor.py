from models import Task
from models import Project
from forms import InboxForm

def tasks_dicts(request):
    r={}
    if request.user.is_authenticated():
        all_my_projects=Project.objects.filter(owner=request.user)
        open_projects=all_my_projects.filter(is_closed=False)

        #~ COLECCIONES
        active_tasks = Task.objects.filter(is_archived=False, is_blocked=False, is_delayed=False)
        bloqued_tasks = Task.objects.filter(is_blocked=True)
        delayed_tasks = Task.objects.filter(is_delayed=True)

        #~ FILTROS
        current_project = request.session.get('current_project')
        filter_highlighted = request.session.get('filter_highlighted')
        
        #~ pending_list = []
        pending_list = active_tasks.order_by('size','project')
        #~ pending_list.append({'label':'- de 5 min','list':active_tasks.filter(size=1)})
        #~ pending_list.append({'label':'+ de 5 min','list':active_tasks.filter(size=2)})
        #~ pending_list.append({'label':'+ de 2 horas','list':active_tasks.filter(size=3)})
        #~ pending_list.append({'label':'?','list':active_tasks.filter(size=4)})
        
        #~ if current_project:
            #~ for qs in pending_list:
                #~ qs['list']=qs['list'].filter(project=current_project)
            #~ bloqued_tasks=bloqued_tasks.filter(project=current_project)
            #~ delayed_tasks=delayed_tasks.filter(project=current_project)
        #~ else:
            #~ for qs in pending_list:
                #~ qs['list']=qs['list'].filter(project__in=open_projects)
            #~ bloqued_tasks=bloqued_tasks.filter(project__in=open_projects)
            #~ delayed_tasks=delayed_tasks.filter(project__in=open_projects)
            #~ 
        #~ if filter_highlighted == '1':
            #~ for qs in pending_list:
                #~ qs['list']=qs['list'].filter(is_highlighted=True)
            #~ bloqued_tasks=bloqued_tasks.filter(is_highlighted=True)
            #~ delayed_tasks=delayed_tasks.filter(is_highlighted=True)

        r['inbox_list']=active_tasks.filter(size=0)
        r['bloqued_tasks']=bloqued_tasks
        r['delayed_tasks']=delayed_tasks
        
        r['inbox_form']=InboxForm()
        r['archived_tasks']=Task.objects.filter(is_archived=True)
        
        lasts_access = open_projects
        if current_project:
            lasts_access = open_projects.exclude(id=current_project.id)
        lasts_access = lasts_access.order_by('-last_access')[0:5]
            
        r['open_projects']=open_projects
        r['all_my_projects']=all_my_projects
        r['current_project']=current_project
        r['filter_highlighted']=filter_highlighted
        r['pending_list'] = pending_list
        r['lasts_access'] = lasts_access
    return r
