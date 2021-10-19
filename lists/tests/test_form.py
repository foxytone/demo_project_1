from typing import Dict
from django.contrib.auth.models import User
from .base import BaseTest
from ..forms import TaskForm, ListForm, ERROR_MESSAGE_EMPTY_TASK_FIELD, ERROR_MESSAGE_DUPLICATED_TASK, \
    ERROR_MESSAGE_EMPTY_LIST_FIELD
from ..models import Task, List


class TaskFormTest(BaseTest):
    def test_form_correct_renders_elements(self):
        form = TaskForm(for_list=self.create_new_list('Matrix', self.Neo))
        
        self.assertIn('placeholder="Enter your task here"', form.as_p())
        self.assertIn('class="form-control input-lg', form.as_p())
        self.assertIn('id="task_form"', form.as_p())
    
    
    def test_form_validation_for_an_empty_task(self):
        form = TaskForm(data={'text': '', }, for_list=self.create_new_list('Matrix', self.Neo))
        self.assertFalse(form.is_valid())
    
    
    def test_form_register_an_empty_task_error(self):
        form = TaskForm(data={'text': ''}, for_list=self.create_new_list('Matrix', self.Neo))
        self.assertEqual(form.errors['text'], [ERROR_MESSAGE_EMPTY_TASK_FIELD], form.errors['text'])
    
    
    # TODO check this
    def test_not_register_an_error_if_proper_task(self):
        form = TaskForm(data={'text': 'A new task!'}, for_list=self.create_new_list('Matrix', self.Neo))
        with self.assertRaises(KeyError):
            form.errors['text']
    
    
    # TODO check this too
    def test_form_register_a_duplicated_task(self):
        list_ = self.create_new_list('Matrix', self.Neo)
        
        task_text = 'A new task!'
        Task.objects.create(text=task_text, list=list_)
        form = TaskForm(data={'text': task_text}, for_list=list_)
        
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [ERROR_MESSAGE_DUPLICATED_TASK])
    
    
    def test_form_can_save_proper_task(self):
        list_ = self.create_new_list('Matrix', self.Neo)
        
        task_text = 'A new task!'
        form = TaskForm(data={'text': task_text}, for_list=list_)
        
        self.assertTrue(form.is_valid())
        
        form.save()
        task = list(Task.objects.all())[0]
        
        self.assertEqual(task.text, task_text)
    
    
    def test_form_cant_save_empty_task(self):
        list_ = self.create_new_list('Matrix', self.Neo)
        
        task_text = ''
        form = TaskForm(data={'text': task_text}, for_list=list_)
        
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()
    
    
    def test_form_cant_save_duplicated_task(self):
        list_ = self.create_new_list('Matrix', self.Neo)
        
        task_text = 'A new task!'
        Task.objects.create(text=task_text, list=list_)
        
        form = TaskForm(data={'text': task_text}, for_list=list_)
        
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()
    
    
    def test_form_can_save_same_tasks_in_different_lists(self):
        list_1 = self.create_new_list('Matrix', self.Neo)
        list_2 = self.create_new_list('Zion', self.Neo)
        
        task_text = 'A new task!'
        
        form1 = TaskForm(data={'text': task_text}, for_list=list_1)
        form2 = TaskForm(data={'text': task_text}, for_list=list_2)
        
        form1.save()
        form2.save()
        
        tasks = list(Task.objects.all())
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].text, tasks[1].text)


class ListFormTest(BaseTest):
    def get_user(self, user: Dict[str, str]) -> User:
        return User.objects.get(username=user['username'])
    
    
    def test_form_correct_renders_elements(self):
        user = self.get_user(self.Neo)
        form = ListForm(user)
        
        self.assertIn('placeholder="Add new list..."', form.as_p())
        self.assertIn('id="list_form"', form.as_p())
    
    
    def test_list_form_validation_for_an_empty_task(self):
        form = ListForm(data={'text': '', }, user=self.get_user(self.Neo))
        self.assertFalse(form.is_valid())
    
    
    def test_form_register_an_empty_list_error(self):
        form = ListForm(data={'text': ''}, user=self.get_user(self.Neo))
        self.assertEqual(form.errors['text'], [ERROR_MESSAGE_EMPTY_LIST_FIELD], form.errors['text'])
    
    
    # TODO check this
    def test_not_register_an_error_if_proper_task(self):
        form = ListForm(data={'text': 'Matrix'}, user=self.get_user(self.Neo))
        with self.assertRaises(KeyError):
            form.errors['text']
    
    
    # TODO check this too
    def test_form_register_a_duplicated_list(self):
        list_ = self.create_new_list('Matrix', self.Neo)
        list_.full_clean()
        list_.save()
        
        form = ListForm(data={'text': 'Matrix'}, user=self.get_user(self.Neo))
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [ERROR_MESSAGE_DUPLICATED_TASK])
    
    
    def test_form_can_save_proper_list(self):
        text = 'Matrix'
        form = ListForm(data={'text': text}, user=self.get_user(self.Neo))
        
        self.assertTrue(form.is_valid())
        
        form.save()
        list_ = list(List.objects.all())[0]
        
        self.assertEqual(list_.text, text)
    
    
    def test_form_cant_save_empty_list(self):
        form = ListForm(data={'text': ''}, user=self.get_user(self.Neo))
        
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()
    
    
    def test_form_cant_save_duplicated_list(self):
        text = 'Matrix'
        list_ = self.create_new_list(text, self.Neo)
        list_.full_clean()
        list_.save()
        form = ListForm(data={'text': text}, user=self.get_user(self.Neo))
        
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()
    
    
    def test_form_can_save_same_lists_for_different_users(self):
        text = 'Shire'
        form1 = ListForm(data={'text': text}, user=self.get_user(self.Neo))
        form2 = ListForm(data={'text': text}, user=self.get_user(self.MisterJones))
        
        form1.save()
        form2.save()
        
        lists = list(List.objects.all())
        self.assertEqual(len(lists), 2)
        self.assertEqual(lists[0].text, lists[1].text)
        self.assertEqual(lists[0].text, text)
