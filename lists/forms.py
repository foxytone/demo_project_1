from django import forms
from lists.models import List, Task
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.exceptions import ValidationError
from django.db import models

ERROR_MESSAGE_EMPTY_TASK_FIELD = "Task can't be empty"
ERROR_MESSAGE_DUPLICATED_TASK = 'You already have this task'
ERROR_MESSAGE_DUPLICATED_LIST = "You already have this list"
ERROR_MESSAGE_EMPTY_LIST_FIELD = "List can't be empty"
ERROR_MESSAGE_MAXIMUM_TASKS_REACHED = "You've reached maximum tasks of 30. Delete one for adding new task"
ERROR_MESSAGE_MAXIMUM_LISTS_REACHED = "You've reached maximum lists of 20. Delete one for adding new list"


class TaskForm(forms.ModelForm):
    def __init__(self, for_list: List, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list
        self.fields['text'].label = False
    
    class Meta:
        # bind with model
        model = Task
        # setup fields. Fields must be like model fields (?)
        # nope, items also can be created in Form class
        fields = ('text',)
        # widgets for fields, keys used as fields
        widgets = {'text': forms.fields.TextInput(attrs={
            'placeholder': 'Enter your task here',
            # 'class': 'form-control input-lg',
            'id': 'task_form',
        })}
        
        # TODO: check required error. Seems like broken. pr
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
    
    
    def is_valid(self) -> bool:
        return super(TaskForm, self).is_valid() & self._not_valid_if_max_tasks_reached()
    
    
    def _not_valid_if_max_tasks_reached(self) -> bool:
        length = len(Task.objects.filter(list=self.instance.list))
        if length > 29:
            e = ValidationError({'text': [ERROR_MESSAGE_MAXIMUM_TASKS_REACHED, ]})
            self._update_errors(e)
            return False
        return True
    
    
    def save(self):
        return forms.ModelForm.save(self)


class ListForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.user = user
        self.fields['text'].label = False
    
    class Meta:
        model = List
        fields = ('text',)
        
        widgets = {'text': forms.fields.TextInput(attrs={
            'placeholder': 'Add new list...',
            'id': 'list_form',
        })}
        
        error_messages = {
            NON_FIELD_ERRORS: {'unique_together': [ERROR_MESSAGE_DUPLICATED_LIST]},
            'text': {'required': [ERROR_MESSAGE_EMPTY_LIST_FIELD], },
        }
    
    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [ERROR_MESSAGE_DUPLICATED_LIST], }
            self._update_errors(e)
    
    
    def is_valid(self):
        return super(ListForm, self).is_valid() & self._not_valid_if_max_lists_reached()
    
    
    def _not_valid_if_max_lists_reached(self) -> bool:
        length = len(List.objects.filter(user=self.instance.user))
        if length > 19:
            self._update_errors(ValidationError({'text': ERROR_MESSAGE_MAXIMUM_LISTS_REACHED}))
            return False
        return True
    
    
    def save(self):
        return forms.ModelForm.save(self)
