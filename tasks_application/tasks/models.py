from django.db import models
from django.contrib.auth.models import User

SIZE_CHOICES = (
    #~ (0, 'Sin definir'),
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
    title = models.CharField(max_length=255, verbose_name='Tarea')
    size = models.IntegerField(default=0, choices=SIZE_CHOICES, verbose_name='Magnitud')
    project = models.ForeignKey(Project, verbose_name='Proyecto')
    detail = models.TextField(max_length=2000,blank=True, null=True, verbose_name='Detalle')
    is_blocked=models.BooleanField(blank=True, default=0, verbose_name='Bloqueada')
    is_archived=models.BooleanField(blank=True, default=0, verbose_name='Archivada')
    is_delayed=models.BooleanField(blank=True, default=0, verbose_name='Pospuesta')
    def __unicode__(self):
        return self.title
