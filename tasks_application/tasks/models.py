from django.db import models

SIZE_CHOICES = (
    (0, 'Sin definir'),
    (1, '< 5 minutos'),
    (2, '> 5 minutos'),
    (3, '> 2 horas'),
    (4, '?'),
)

class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name='Tarea')
    #~ detail = models.TextField(blank=True, null=True)
    is_blocked=models.BooleanField(blank=True, default=0)
    is_archived=models.BooleanField(blank=True, default=0)
    is_closed=models.BooleanField(blank=True, default=0)
    size = models.IntegerField(default=0, choices=SIZE_CHOICES)
    def __unicode__(self):
        return self.title
