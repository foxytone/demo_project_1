from django.test import TestCase
import unittest
from django.contrib.auth.models import User
from .base import BaseTest


class TestTaskView(BaseTest):

    def test_unlogged_page(self):
        response = self.client.get('/tasks/')
        self.assertTrue(response.status_code == 302, response.status_code)


    def test_correct_html_page_with_login_and_list(self):
        self.login(self.MisterJones)
        list_ = self.create_new_list('list1', self.MisterJones)
        self.create_new_task('task1', list_=list_)

        response = self.client.get('/tasks/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/tasks.html')
        self.assertTemplateUsed(response, 'base.html')

        html = response.content.decode('utf-8')
        self.page_correct_tags(html)


    def test_contains_list_form(self):
        self.login(self.MisterJones)
        response = self.client.get('/tasks/')

        self.assertEqual(response.status_code, 200)
        self.assertRegex(expected_regex=r'<form(.|\n)*id="list_form"(.|\n)*/form>',
                         text=response.content.decode('utf-8'),
                         msg='no list form found')


    def test_tasks_representation(self):
        # this one is huge

        # login
        self.login(self.MisterJones)
        response = self.client.get('/tasks/')

        self.assertEqual(response.status_code, 200)

        # crate list and task for it
        list_ = self.create_new_list('new list!', self.MisterJones)
        self.create_new_task('task1', list_)

        # check it's in the list
        text = self.client.get('/tasks/')
        self.assertRegex(expected_regex=r'<td(.|\n)*task1(.|\n)*/td>', text=text.content.decode('utf-8'))
        self.assertRegex(expected_regex=r'<a(.|\n)*list0(.|\n)*/a>', text=text.content.decode('utf-8'))

        # check nothing unusual in the list
        self.assertNotRegex(unexpected_regex=r'<td(.|\n)*task2(.|\n)*/td>', text=text.content.decode('utf-8'))
        self.assertNotRegex(unexpected_regex=r'<a(.|\n)*list1(.|\n)*/a>', text=text.content.decode('utf-8'))

        # create new task and check its' in the list too
        self.create_new_task('task2', list_)

        text = self.client.get('/tasks/')
        self.assertRegex(expected_regex=r'<td(.|\n)*task1(.|\n)*/td>', text=text.content.decode('utf-8'))
        self.assertRegex(expected_regex=r'<a(.|\n)*list0(.|\n)*/a>', text=text.content.decode('utf-8'))
        self.assertRegex(expected_regex=r'<td(.|\n)*task2(.|\n)*/td>', text=text.content.decode('utf-8'))

        # TODO: Add tests for 2nd user


class TestNoListsPage(BaseTest):
    def test_page_for_new_user_contains_only_list_form(self):
        self.login(self.MisterJones)
        response = self.client.get('/tasks/')

        html = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertNotRegex(unexpected_regex=r'<form(.|\n)*id="task_form"(.|\n)*/form>',
                            text=response.content.decode('utf-8'))
        self.assertRegex(expected_regex=r'<form(.|\n)*id="list_form"(.|\n)*/form>',
                         text=response.content.decode('utf-8'))
        self.page_correct_tags(html)
        self.assertRegex(expected_regex='(.|\n)*No task lists found!\n Maybe you should create one?(.|\n)*', text=html)


class TestHomePage(BaseTest):
    def test_unlogged_page(self):
        response = self.client.get('/')
        self.assertTrue(response.status_code == 200)
        html = response.content.decode('utf-8')

        self.page_correct_tags(html)
        self.assertRegex(
            expected_regex='Hello! :\) This is your simple To-Do app!',
            text=html)

        # regex for not-logged homepage
        self.assertRegex(expected_regex=f'Please, <a href="/login/">login</a> or'
                                        f' <a href="/auth/register/">register</a>'
                                        f' to start{self.all_pattern}*use{self.all_pattern}*your tasks', text=html)
