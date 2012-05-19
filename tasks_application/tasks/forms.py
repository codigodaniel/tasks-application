from django.forms import ModelForm
from models import Task

class InboxForm(ModelForm):
    class Meta:
        model = Task
        exclude=['size','is_blocked','is_archived','is_closed',]

class TaskForm(ModelForm):
    class Meta:
        model = Task
