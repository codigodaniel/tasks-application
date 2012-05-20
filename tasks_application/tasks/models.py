from django.db import models
from django.contrib.auth.models import User

SIZE_CHOICES = (
    (0, 'Sin definir'),
    (1, '- de 5 minutos'),
    (2, '+ de 5 minutos'),
    (3, '+ de 2 horas'),
    (4, '?'),
)

class Project(models.Model):
    owner = models.ForeignKey(User, verbose_name='Usuario')
    title = models.CharField(max_length=255, verbose_name='Nombre')
    is_closed=models.BooleanField(blank=True, default=0, verbose_name='Cerrado')
    def __unicode__(self):
        return self.title

class Task(models.Model):
    project = models.ForeignKey(Project,blank=True, null=True)
    title = models.CharField(max_length=255, verbose_name='Tarea')
    #~ detail = models.TextField(blank=True, null=True)
    is_blocked=models.BooleanField(blank=True, default=0)
    is_archived=models.BooleanField(blank=True, default=0)
    is_closed=models.BooleanField(blank=True, default=0)
    size = models.IntegerField(default=0, choices=SIZE_CHOICES)
    def __unicode__(self):
        return self.title
