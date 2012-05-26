from django.forms import ModelForm
from models import Task
from models import Project
from models import SIZE_CHOICES
from django.forms.widgets import RadioSelect
from django.forms.fields import ChoiceField

from django.forms import Textarea

class InboxForm(ModelForm):
    class Meta:
        model = Task
        exclude=['size','is_blocked','is_archived','is_delayed','project']

class TaskForm(ModelForm):
    size = ChoiceField(widget=RadioSelect, choices=SIZE_CHOICES, label='Magnitud')
    class Meta:
        model = Task
        widgets = {
            'project': RadioSelect(),
        }

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude=['owner','is_closed']
