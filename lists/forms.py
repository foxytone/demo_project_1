from django import forms
from lists.models import List, Task


class TaskForm(forms.models.ModelForm):
    class Meta:
        model = Task
        fields = ('text',)
        widgets = {'text': forms.fields.TextInput(attrs={
            'placeholder': 'Enter your task here',
            'class': 'form-control input-lg',
            'id': 'task_form'
        })}
