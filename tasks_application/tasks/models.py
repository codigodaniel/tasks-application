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
    def get_or_create_by_owner_and_title(self,owner,title):
        p = None
        ps = self.filter(owner = owner).filter(title = title)
        if ps:
            p = ps[0]
        else:
            if title:
                p = self.model(title = title,owner = owner)
                p.save()
        return p


class Project(models.Model):
    owner = models.ForeignKey(User, verbose_name = 'Usuario')
    title = models.CharField(max_length = 255, verbose_name = 'Nombre')
    is_closed = models.BooleanField(blank = True, default = 0, verbose_name = 'Cerrado')
    last_access = models.DateTimeField(auto_now_add = True, null = True)
    
    objects = ProjectManager()
    
    def to_json(self):
        return '{"title":"'+self.title+'"}'
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
    
    def absolute_url(self):
        return reverse('tasks_task_edit', args = [self.id])
        
    def __unicode__(self):
        return self.title
