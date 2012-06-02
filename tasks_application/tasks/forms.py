from django.forms import ModelForm
from models import Task
from models import Project
from models import SIZE_CHOICES
from django.forms.widgets import RadioSelect, TextInput, HiddenInput
from django.forms.fields import ChoiceField, CharField

from django.forms import Textarea

class InboxForm(ModelForm):
    class Meta:
        model = Task
        exclude=['size','is_blocked','is_archived','is_delayed','project']

class TaskForm(ModelForm):
    project_title = CharField(widget=TextInput, label='Proyecto')
    size = ChoiceField(widget=RadioSelect, choices=SIZE_CHOICES, label='Magnitud')
    class Meta:
        model = Task
        widgets = {
            'project': HiddenInput(),
        }
        fields = ['project','project_title','title','size','detail','is_blocked','is_archived','is_delayed']

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude=['owner','is_closed']
