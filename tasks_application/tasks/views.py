from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Task
from models import Project
from forms import InboxForm
from forms import TaskForm
from django.core.urlresolvers import reverse

from django.views.generic.create_update import get_model_and_form_class, lookup_object
from django.views.generic.create_update import redirect
from django.utils.translation import ugettext
from django.contrib import messages

from django.contrib.auth.decorators import login_required

def index(request):
    r={}
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
    r={}
    r['inbox_list']=Task.objects.filter(size=0)
    inbox_first=None
    if r['inbox_list']:
        inbox_first=r['inbox_list'][0]
    r['form']=TaskForm(instance=inbox_first)
    r['inbox_first']=inbox_first
    if inbox_first:
        return render_to_response('tasks/process.html', r, RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('tasks_home'))

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

def task_duplicate(request, object_id):
    try:
        obj=Task.objects.get(pk=object_id)
        obj.pk=None
        obj.save()
    except:
        pass
    return HttpResponseRedirect(reverse('tasks_home'))

def create_user_owned_object(request, 
    model=None, 
    template_name=None,
        #~ template_loader=loader, 
        extra_context=None, 
        post_save_redirect=None,
        login_required=False, 
        context_processors=None, 
        form_class=None):
    """
    """
    if extra_context is None: extra_context = {}
    if login_required and not request.user.is_authenticated():
        return redirect_to_login(request.path)

    model, form_class = get_model_and_form_class(model, form_class)
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            #~ new_object = Task()
            new_object = form.save(commit=False)
            #~ relation with session user
            new_object.owner=request.user
            new_object.save()

            msg = ugettext("The %(verbose_name)s was created successfully.") %\
                                    {"verbose_name": model._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
            return redirect(post_save_redirect, new_object)
    else:
        form = form_class()

    # Create the template, context, response
    if not template_name:
        template_name = "%s/%s_form.html" % (model._meta.app_label, model._meta.object_name.lower())
        
    return render_to_response(template_name, {'form': form}, RequestContext(request))
    
def task_archived(request):
    r={}
    r['form']=InboxForm()
    r['archived_tasks']=Task.objects.filter(is_archived=True)
    return render_to_response('tasks/task_archived.html', r, RequestContext(request))




    if not template_name:
        template_name = "%s/%s_form.html" % (model._meta.app_label, model._meta.object_name.lower())
    t = template_loader.get_template(template_name)
    c = RequestContext(request, {
        'form': form,
        template_object_name: obj,
    }, context_processors)
    apply_extra_context(extra_context, c)
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, model, getattr(obj, obj._meta.pk.attname))
    return response

def save_or_continue_editing(request, 
        model=None, object_id=None, slug=None,
        slug_field='slug', template_name=None,
         #~ template_loader=loader,
        extra_context=None, post_save_redirect=None, login_required=False,
        context_processors=None, template_object_name='object',
        form_class=None):
    """
    """
    if extra_context is None: extra_context = {}
    if login_required and not request.user.is_authenticated():
        return redirect_to_login(request.path)
    model, form_class = get_model_and_form_class(model, form_class)
    obj = lookup_object(model, object_id, slug, slug_field)

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save()
            msg = ugettext("The %(verbose_name)s was updated successfully.") %\
                                    {"verbose_name": model._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
        if "_continue" not in request.POST:
            return redirect(post_save_redirect, obj)
    else:
        form = form_class(instance=obj)
    if not template_name:
        template_name = "%s/%s_form.html" % (model._meta.app_label, model._meta.object_name.lower())
    return render_to_response(template_name, {'form': form,'object':obj}, RequestContext(request))
