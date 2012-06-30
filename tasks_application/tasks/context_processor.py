from models import Task
from models import Project
from forms import InboxForm

def tasks_dicts(request):
    r={}
    if request.user.is_authenticated():
        all_my_projects=Project.objects.filter(owner=request.user)
        all_my_open_projects=all_my_projects.filter(is_closed=False)

        #~ COLECCIONES
        active_tasks = Task.objects.filter(is_archived=False, is_blocked=False, is_delayed=False).filter(project__in=all_my_open_projects)
        visible_tasks = Task.objects.filter(is_archived=False).filter(project__in=all_my_open_projects).filter(size__gt=0)
        
        #~ FILTROS
        current_project = request.session.get('current_project')
        filter_highlighted = request.session.get('filter_highlighted')
        
        if current_project:
            visible_tasks=visible_tasks.filter(project=current_project)

        if filter_highlighted == '1':
            visible_tasks=visible_tasks.filter(is_highlighted=True)
        
        #~ ordering
        visible_tasks=visible_tasks.order_by('size','project')
            
        #~ extrayendo bloqueadas y postergadas
        bloqued_tasks = visible_tasks.filter(is_blocked=True)
        delayed_tasks = visible_tasks.filter(is_delayed=True)
        
        #~ ahora trabajo sin bloqueadas ni postergadas
        visible_tasks = visible_tasks.filter(is_delayed=False).filter(is_blocked=False)

        #~ filtro por sizes
        size_1_tasks = visible_tasks.filter(size=1)
        size_2_tasks = visible_tasks.filter(size=2)
        size_3_tasks = visible_tasks.filter(size=3)
        size_4_tasks = visible_tasks.filter(size=4)
        
        filtered_lists = [size_1_tasks,size_2_tasks,size_3_tasks,size_4_tasks, bloqued_tasks, delayed_tasks]

        r['inbox_list']=active_tasks.filter(size=0)
        r['bloqued_tasks']=bloqued_tasks
        r['delayed_tasks']=delayed_tasks
        
        r['inbox_form']=InboxForm()
        r['archived_tasks']=Task.objects.filter(is_archived=True)
        
        lasts_access = all_my_open_projects
        if current_project:
            lasts_access = all_my_open_projects.exclude(id=current_project.id)
        lasts_access = lasts_access.order_by('-last_access')[0:5]
            
        r['all_my_open_projects']=all_my_open_projects
        r['all_my_projects']=all_my_projects
        r['current_project']=current_project
        r['filter_highlighted']=filter_highlighted
        r['filtered_lists'] = filtered_lists
        r['lasts_access'] = lasts_access
    return r
