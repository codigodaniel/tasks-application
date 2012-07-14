from django.db import models
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

SIZE_CHOICES = (
    #~ (0, 'In Box'),
    (1, '- de 5 minutos'),
    (2, '+ de 5 minutos'),
    (3, '+ de 2 horas'),
    (4, '?'),
)

#~ :D
class ProjectManager(models.Manager):
    
    def get_or_create_by_owner_and_title(self, owner, title):
        p = None
        ps = self.filter(owner = owner).filter(title = title)
        if ps:
            p = ps[0]
        else:
            if title:
                p = self.model(title = title,owner = owner)
                p.save()
        return p


class TaskManager(models.Manager):
    
    def toggle_highlight(self, object_id):
        try:
            obj = Task.objects.get(pk = object_id)
            obj.toggle_highlight()
        except:
            pass
            
    def toggle_block(self, object_id):
        try:
            obj = Task.objects.get(pk = object_id)
            obj.toggle_block()
        except:
            pass
        
    def toggle_archived(self, object_id):
        try:
            obj = Task.objects.get(pk = object_id)
            obj.toggle_archived()
            return obj
        except:
            pass
    
    def toggle_delay(self, object_id):
        try:
            obj = Task.objects.get(pk = object_id)
            obj.toggle_delay()
        except:
            pass

    def duplicate(self, object_id):
        try:
            obj = self.get(pk = object_id)
            obj.pk = None
            obj.title = 'Copia de: '+obj.title
            obj.save()
        except:
            pass
        return obj


class Project(models.Model):
    owner = models.ForeignKey(User, verbose_name = 'Usuario')
    title = models.CharField(max_length = 255, verbose_name = 'Nombre')
    is_closed = models.BooleanField(blank = True, default = 0, verbose_name = 'Cerrado')
    last_access = models.DateTimeField(auto_now_add = True, null = True)
    
    objects = ProjectManager()
    
    def to_json(self):
        return '{"title":"'+self.title+'"}'

    def count_tasks(self):
        return self.task_set.all().count()
        
    def __unicode__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length = 255, verbose_name = 'Tarea')
    size = models.IntegerField(default = 0, choices = SIZE_CHOICES, verbose_name = 'Magnitud')
    project = models.ForeignKey(Project, verbose_name = 'Proyecto',blank = True, null = True, default = '')
    detail = models.TextField(max_length = 2000,blank = True, null = True, verbose_name = 'Detalle')
    is_blocked = models.BooleanField(blank = True, default = 0, verbose_name = 'Bloqueada')
    is_archived = models.BooleanField(blank = True, default = 0, verbose_name = 'Archivada')
    is_delayed = models.BooleanField(blank = True, default = 0, verbose_name = 'Pospuesta')
    is_highlighted = models.BooleanField(blank = True, default = 0, verbose_name = 'Destacada')
            
    objects = TaskManager()
    
    def toggle_block(self):
        if self.is_blocked:
            self.is_blocked = False
        else:
            self.is_blocked = True
        self.save()
        
    def toggle_archived(self):
        if self.is_archived == False:
            self.is_archived = True
            self.is_delayed = False
            self.is_highlighted = False
            self.is_blocked = False
        else:
            self.is_archived = False
        self.save()
        
    def toggle_delay(self):
        if self.is_delayed:
            self.is_delayed = False
        else:
            self.is_delayed = True
        self.save()
        
    def toggle_highlight(self):
        if self.is_highlighted:
            self.is_highlighted = False
        else:
            self.is_highlighted = True
        self.save()
        
    def absolute_url(self):
        return reverse('tasks_task_edit', args = [self.id])
        
    def __unicode__(self):      
        return self.title

