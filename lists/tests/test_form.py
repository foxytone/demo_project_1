from django.test import TestCase
from ..forms import TaskForm, ERROR_MESSAGE_EMPTY_TASK_FIELD, ERROR_MESSAGE_DUPLICATED_TASK
from ..models import List, Task


class TaskFormTest(TestCase):
    def get_list(self, num: str = ''):
        return List.objects.create(text=f'A new list!{num}')


    def test_form_correct_renders_elements(self):
        form = TaskForm(for_list=self.get_list())

        self.assertIn('placeholder="Enter your task here"', form.as_p())
        self.assertIn('class="form-control input-lg', form.as_p())
        self.assertIn('id="task_form"', form.as_p())


    def test_form_validation_for_an_empty_task(self):
        form = TaskForm(data={'text': '', }, for_list=self.get_list())
        self.assertFalse(form.is_valid())


    def test_form_register_an_empty_task_error(self):
        form = TaskForm(data={'text': ''}, for_list=self.get_list())
        self.assertEqual(form.errors['text'], [ERROR_MESSAGE_EMPTY_TASK_FIELD], form.errors['text'])


    def test_not_register_an_error_if_proper_task(self):
        form = TaskForm(data={'text': 'A new task!'}, for_list=self.get_list())
        with self.assertRaises(KeyError):
            form.errors['text']


    def test_form_register_a_duplicated_task(self):
        list_ = self.get_list()

        task_text = 'A new task!'
        Task.objects.create(text=task_text, list=list_)
        form = TaskForm(data={'text': task_text}, for_list=list_)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [ERROR_MESSAGE_DUPLICATED_TASK])


    def test_form_can_save_proper_task(self):
        list_ = self.get_list()

        task_text = 'A new task!'
        form = TaskForm(data={'text': task_text}, for_list=list_)

        self.assertTrue(form.is_valid())

        form.save()
        task = list(Task.objects.all())[0]

        self.assertEqual(task.text, task_text)


    def test_form_cant_save_empty_task(self):
        list_ = self.get_list()

        task_text = ''
        form = TaskForm(data={'text': task_text}, for_list=list_)

        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()


    def test_form_cant_save_duplicated_task(self):
        list_ = self.get_list()

        task_text = 'A new task!'
        Task.objects.create(text=task_text, list=list_)

        form = TaskForm(data={'text': task_text}, for_list=list_)

        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()


    def test_form_can_save_same_tasks_in_different_lists(self):
        list_1 = self.get_list()
        list_2 = self.get_list(num='2')

        task_text = 'A new task!'

        form1 = TaskForm(data={'text': task_text}, for_list=list_1)
        form2 = TaskForm(data={'text': task_text}, for_list=list_2)

        form1.save()
        form2.save()

        tasks = list(Task.objects.all())
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].text, tasks[1].text)
