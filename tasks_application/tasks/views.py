from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Task
from models import Project

from forms import TaskForm
from forms import ProjectForm
from django.core.urlresolvers import reverse

from django.views.generic.create_update import get_model_and_form_class, lookup_object
from django.views.generic.create_update import redirect
from django.utils.translation import ugettext
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from datetime import datetime

def index(request):
    r = {}
    return render_to_response('tasks/home.html', r, RequestContext(request))

def project_set(request, object_id):
    try:
        obj = Project.objects.get(pk = object_id)
        obj.last_access = datetime.now()
        request.session['current_project'] = obj
        obj.save()
    except:
        request.session['current_project'] = None
        pass
    return HttpResponseRedirect(reverse('tasks_home'))
    
def process(request):
    r = {}
    r['inbox_list'] = Task.objects.filter(size = 0)
    inbox_first = None
    if r['inbox_list']:
        inbox_first = r['inbox_list'][0]
    r['form'] = TaskForm(instance = inbox_first)
    r['inbox_first'] = inbox_first
    if inbox_first:
        return render_to_response('tasks/process.html', r, RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('tasks_home'))

def task_delay(request, object_id):
    try:
        obj = Task.objects.get(pk = object_id)
        obj.change_delay()
    except:
        pass
    return HttpResponseRedirect(reverse('tasks_home'))
    
def task_archive(request, object_id):
    try:
        obj = Task.objects.get(pk = object_id)
        obj.change_archive()
    except:
        pass
    return HttpResponseRedirect(reverse('tasks_home'))

def task_block(request, object_id):
    try:
        obj = Task.objects.get(pk = object_id)
        obj.change_block()
    except:
        pass
    return HttpResponseRedirect(reverse('tasks_home'))
    
def task_highlight(request, object_id):
    try:
        obj = Task.objects.get(pk = object_id)
        obj.change_highlight()
    except:
        pass
    return HttpResponseRedirect(reverse('tasks_home'))

def task_duplicate(request, object_id):
    obj = Task.objects.duplicate(object_id)
    if obj:
        return HttpResponseRedirect(reverse('tasks_task_edit', kwargs={'object_id': obj.id}))
    else:
        return HttpResponseRedirect(reverse('tasks_home'))
    
def task_detail(request, object_id):
    try:
        r = {}
        r['object'] = Task.objects.get(pk = object_id)
    except:
        pass
    return render_to_response('tasks/task_detail.html', r, RequestContext(request))
    
def project_close(request, object_id):
    try:
        obj = Project.objects.get(pk = object_id)
        if obj.is_closed:
            obj.is_closed = False
        else:
            obj.is_closed = True 
        obj.save()
        if obj  ==  request.session.get('current_project'):
            return project_set(request, object_id = 0)
    except:
        pass
    return HttpResponseRedirect(reverse('tasks_project_general'))

def project_general(request):
    r = {}
    r['form'] = ProjectForm()
    r['project_list'] = Project.objects.filter(owner = request.user)
    return render_to_response('tasks/project_general.html', r, RequestContext(request))

def create_user_owned_object(request, 
                             model = None,template_name = None,
                             extra_context = None, post_save_redirect = None,
                             login_required = False, context_processors = None, 
                             form_class = None):
    if extra_context is None: extra_context = {}
    if login_required and not request.user.is_authenticated():
        return redirect_to_login(request.path)

    model, form_class = get_model_and_form_class(model, form_class)
    if request.method  ==  'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            #~ new_object = Task()
            new_object = form.save(commit = False)
            #~ relation with session user
            new_object.owner = request.user
            new_object.save()

            msg = ugettext("The %(verbose_name)s was created successfully.") %\
                                    {"verbose_name": model._meta.verbose_name}
            messages.success(request, msg, fail_silently = True)
            return redirect(post_save_redirect, new_object)
    else:
        form = form_class()

    # Create the template, context, response
    if not template_name:
        template_name = "%s/%s_form.html" % (model._meta.app_label, model._meta.object_name.lower())
        
    return render_to_response(template_name, {'form': form}, RequestContext(request))

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

def task_update(request, model = None, 
                object_id = None, slug = None,
                slug_field = 'slug', template_name = None,
                extra_context = None, post_save_redirect = None, 
                login_required = False, context_processors = None, 
                template_object_name = 'object',form_class = None):
    if extra_context is None: extra_context = {}
    if login_required and not request.user.is_authenticated():
        return redirect_to_login(request.path)
    model, form_class = get_model_and_form_class(model, form_class)
    obj = lookup_object(model, object_id, slug, slug_field)

    if request.method == 'POST':
        #~ recuperar o crear el proyecto
        p = Project.objects.get_or_create_by_owner_and_title(request.user,request.POST.get('project_title'))
        form = form_class(request.POST, request.FILES, instance = obj)
        del form.fields['project']
        if form.is_valid():
            obj = form.save(commit = False)
            obj.project = p
            obj.save()
            msg = ugettext("The %(verbose_name)s was updated successfully.") %\
                                    {"verbose_name": model._meta.verbose_name}
            messages.success(request, msg, fail_silently = True)
            if "_continue" not in request.POST:
                return redirect(post_save_redirect, obj)
    else:
        form = form_class(instance = obj)
    if not template_name:
        template_name = "%s/%s_form.html" % (model._meta.app_label, model._meta.object_name.lower())
    return render_to_response(template_name, {'form': form,'object':obj}, RequestContext(request))

def task_create(request, model = None,  
                template_name = None, extra_context = None, 
                post_save_redirect = None, login_required = False, 
                context_processors = None, form_class = None):
    if extra_context is None: extra_context = {}
    if login_required and not request.user.is_authenticated():
        return redirect_to_login(request.path)

    model, form_class = get_model_and_form_class(model, form_class)
    if request.method  ==  'POST':
        p = Project.objects.get_or_create_by_owner_and_title(request.user,request.POST.get('project_title_inbox'))
        form = form_class(request.POST, request.FILES)
        #~ del form.fields['project']
        if form.is_valid():
            #~ new_object = Task()
            new_object = form.save(commit = False)
            new_object.project = p
            new_object.save()
            msg = ugettext("The %(verbose_name)s was created successfully.") %\
                                    {"verbose_name": model._meta.verbose_name}
            messages.success(request, msg, fail_silently = True)
            return redirect(post_save_redirect, new_object)
    else:
        form = form_class()
    if not template_name:
        template_name = "%s/%s_form.html" % (model._meta.app_label, model._meta.object_name.lower())
    return render_to_response(template_name, {'form': form}, RequestContext(request))

def project_json(request):
    r = {}
    if request.method  ==  'GET':
        q = request.GET.get('q')
        #~ from django.core import serializers
        #~ data = serializers.serialize("json", )
        r['object_list'] = Project.objects.filter(owner = request.user).filter(is_closed = False).filter(title__contains = q)
        pass
    return render_to_response('tasks/project_json.html', r, RequestContext(request))

def task_json(request):
    r = {}
    if request.method  ==  'GET':
        q = request.GET.get('q')
        project_list = Project.objects.filter(owner = request.user)
        pre_list = Task.objects.filter(project__in = project_list)
        pre_list1 = pre_list.filter(title__contains = q)
        pre_list2 = pre_list.filter(detail__contains = q)
        #~ r['object_list'] = Task.objects.filter(title__contains = q)
        r['object_list'] = pre_list1 | pre_list2
        # filtrar por detail
        pass
    return render_to_response('tasks/task_json.html', r, RequestContext(request))

def filter_highlighted(request, value):
    request.session['filter_highlighted'] = value
    return HttpResponseRedirect(reverse('tasks_home'))
