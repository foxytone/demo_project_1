from django import forms
from lists.models import List, Task
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.exceptions import ValidationError

ERROR_MESSAGE_EMPTY_TASK_FIELD = "Task can't be empty"
ERROR_MESSAGE_DUPLICATED_TASK = 'You already have this task'


class TaskForm(forms.ModelForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    class Meta:
        # bind with model
        model = Task
        # setup fields. Fields must be like model fields (?)
        fields = ('text',)
        # widgets for fields, keys used as fields
        widgets = {'text': forms.fields.TextInput(attrs={
            'placeholder': 'Enter your task here',
            'class': 'form-control input-lg',
            'id': 'task_form',
        })}
        error_messages = {
            NON_FIELD_ERRORS: {'unique_together': [ERROR_MESSAGE_DUPLICATED_TASK]},
            'text': {'required': [ERROR_MESSAGE_EMPTY_TASK_FIELD], },
        }

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [ERROR_MESSAGE_DUPLICATED_TASK], }
            self._update_errors(e)
