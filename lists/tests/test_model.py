from django.test import TestCase
from ..models import Task, List
from django.core.exceptions import ValidationError


class TaskModelTest(TestCase):
    def test_can_properly_save_task(self):
        # we need to create a list for a task obv
        list_1 = List.objects.create(text='Needs')

        text_for_task_1 = 'My first task'
        text_for_task_2 = 'SECOND'
        text_for_task_3 = 'Hello, need YET ANOTHER AMAZING TASK MANAGER'

        task_1 = Task(text=text_for_task_1, list=list_1)
        task_2 = Task(text=text_for_task_2, list=list_1)
        task_3 = Task(text=text_for_task_3, list=list_1)

        task_1.full_clean()
        task_2.full_clean()
        task_3.full_clean()

        task_1.save()
        task_2.save()
        task_3.save()

        q_set = list(Task.objects.all())

        self.assertEqual(len(q_set), 3, q_set)

        self.assertIn(task_1, q_set)
        self.assertIn(task_2, q_set)
        self.assertIn(task_3, q_set)

        q_set = Task.objects.all().order_by('id')

        self.assertEqual(task_1, q_set[0])
        self.assertEqual(task_2, q_set[1])
        self.assertEqual(task_3, q_set[2])


    def test_cant_save_empty_task(self):
        list_1 = List.objects.create(text='List1')

        with self.assertRaises(ValidationError):
            task_1 = Task(text='', list=list_1)
            task_1.full_clean()


    def test_cant_save_duplicated_tasks_in_one_list(self):
        list_1 = List.objects.create(text='List1')

        text = 'Duplicated'

        Task.objects.create(text=text, list=list_1)
        with self.assertRaises(ValidationError):
            task_2 = Task(text=text, list=list_1)
            task_2.full_clean()


    def test_can_save_duplicated_tasks_in_different_lists(self):
        list_1 = List.objects.create(text='List1')
        list_2 = List.objects.create(text='List2')

        text = 'Duplicated'

        Task.objects.create(text=text, list=list_1)
        task_2 = Task(text=text, list=list_2)
        task_2.full_clean()


class ListModelTest(TestCase):
    def test_can_properly_save_list(self):
        list_1 = List.objects.create(text='blabla')
        list_2 = List.objects.create(text='HELLO!')
        list_3 = List.objects.create(text='LIST 3!')

        q_set = list(List.objects.all().order_by('id'))

        self.assertEqual(len(q_set), 3)

        self.assertIn(list_1, q_set)
        self.assertIn(list_2, q_set)
        self.assertIn(list_3, q_set)

        q_set = List.objects.all().order_by('id')

        self.assertEqual(list_1, q_set[0])
        self.assertEqual(list_2, q_set[1])
        self.assertEqual(list_3, q_set[2])


    def test_cant_save_duplicated_lists(self):
        text = 'Duplicated'
        List.objects.create(text=text)
        with self.assertRaises(ValidationError):
            list_2 = List(text=text)
            list_2.full_clean()

    def test_cant_save_empty_list(self):
        with self.assertRaises(ValidationError):
            list_1 = List(text='')
            list_1.full_clean()
