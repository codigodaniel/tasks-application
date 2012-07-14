from django.forms import ModelForm
from models import Task
from models import Project
from models import SIZE_CHOICES
from django.forms.widgets import RadioSelect, TextInput, HiddenInput
from django.forms.fields import ChoiceField, CharField

from django.forms import Textarea

project_title_field = CharField(widget = TextInput, label = 'Carpeta', required = True)

class InboxForm(ModelForm):
    project_title_inbox = project_title_field
    
    class Meta:
        model = Task
        exclude = ['size', 'is_blocked', 'is_archived', 'is_delayed', 'project', 'is_highlighted']
        fields = ['project', 'project_title_inbox', 'title', 'size', 'is_highlighted', 'detail', 'is_blocked', 'is_archived', 'is_delayed']

class TaskForm(ModelForm):
    project_title = project_title_field
    project = CharField(widget = HiddenInput, required = False)
    size = ChoiceField(widget = RadioSelect, choices = SIZE_CHOICES, label = 'Magnitud')
    
    class Meta:
        model = Task
        #~ widgets = {
            #~ 'project': HiddenInput(), 
        #~ }
        fields = ['project', 'project_title', 'title', 'size', 'is_highlighted', 'detail', 'is_blocked', 'is_archived', 'is_delayed']

class ProjectForm(ModelForm):
    
    class Meta:
        model = Project
        exclude = ['owner', 'is_closed']
