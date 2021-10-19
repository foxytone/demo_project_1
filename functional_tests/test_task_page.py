from .base import BaseTest
from selenium.common.exceptions import WebDriverException


# TODO: add errors pop up and remove function for tasks and lists and limit for tasks and lists
class TestTaskPage(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        
        # init a user
        self.tasks_url = self.live_server_url + '/tasks/'
        self.register_user(self.MisterJones)
    
    
    def add_list(self, list_name: str) -> None:
        listbox = self.browser.find_element_by_id('list_form')
        self.send_info(listbox, list_name)
    
    
    def add_task(self, task_name: str) -> None:
        taskbox = self.browser.find_element_by_id('task_form')
        self.send_info(taskbox, task_name)
    
    
    def test_proper_task_page(self):
        self.browser.get(self.tasks_url)
        header = self.wait_for(lambda: self.browser.find_element_by_id('header'))
        self.assertTrue(header.text == "No task lists found! Maybe you should create one?")
        
        # no task form with empty list
        with self.assertRaises(WebDriverException):
            self.browser.find_element_by_id('task_form')
        
        # and form for lists adding
        self.browser.find_element_by_id('list_form')
    
    
    def test_add_a_task_on_starter_task_page(self):
        # This one is huge
        self.browser.get(self.tasks_url)
        
        # add first list
        
        first_list_name = 'Chapter One'
        self.browser.get(self.tasks_url)
        self.wait_for(lambda: self.browser.find_element_by_id('list_form'))
        self.add_list(first_list_name)
        
        # check for this list
        list1 = self.wait_for(lambda: self.browser.find_element_by_id('id_list0'))
        self.assertTrue(list1.text == first_list_name)
        
        # add task
        first_task_name = 'My first task!'
        self.add_task(first_task_name)
        
        # wait for task pop up
        task0 = self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        self.assertTrue(task0.text == first_task_name)
        
        # add another task
        second_task_name = 'My second task!'
        self.add_task(second_task_name)
        
        # wait for both tasks pop up and check them
        task0 = self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        task1 = self.browser.find_element_by_id('task1')
        self.assertTrue(task0.text == second_task_name)
        self.assertTrue(task1.text == first_task_name)
        
        # check that no another tasks
        with self.assertRaises(WebDriverException):
            self.browser.find_element_by_id('task2')
        with self.assertRaises(WebDriverException):
            self.browser.find_element_by_id('list1')
        
        # add second list
        second_list_name = 'My second list!'
        self.add_list(second_list_name)
        
        # check for 2 lists
        list0 = self.wait_for(lambda: self.browser.find_element_by_id('id_list0'))
        list1 = self.browser.find_element_by_id('id_list1')
        self.assertTrue(list1.text == first_list_name)
        self.assertTrue(list0.text == second_list_name)
        
        # check tasks is empty
        with self.assertRaises(WebDriverException):
            self.wait_for(lambda: self.browser.find_element_by_id(first_task_name))
        with self.assertRaises(WebDriverException):
            self.browser.find_element_by_id(second_task_name)
        
        # add new task:
        third_task_name = 'My third task!'
        self.add_task(third_task_name)
        
        # waif for task pop up and check it
        task3 = self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        self.assertTrue(task3.text == third_task_name)
        
        # one more check for tasks in another list:
        with self.assertRaises(WebDriverException):
            self.wait_for(lambda: self.browser.find_element_by_id('task1'))
        with self.assertRaises(WebDriverException):
            self.browser.find_element_by_id('task2')
        
        # switch to the first list:
        self.browser.find_element_by_id('id_list1').click()
        
        # check for two first tasks:
        task0 = self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        task1 = self.browser.find_element_by_id('task1')
        self.assertTrue(task1.text == first_task_name)
        self.assertTrue(task0.text == second_task_name)
        
        # check for 2 lists
        
        list1 = self.wait_for(lambda: self.browser.find_element_by_id('id_list1'))
        list0 = self.browser.find_element_by_id('id_list0')
        self.assertTrue(list1.text == first_list_name)
        self.assertTrue(list0.text == second_list_name)
        
        # check that third task is not exist here
        with self.assertRaises(WebDriverException):
            self.wait_for(lambda: self.browser.find_element_by_id(third_task_name))
        
        ## ! checkout for other user
        
        self.browser.get(self.live_server_url + '/logout/')
        self.register_user(self.Neo)
        
        # he has no previous tasks
        with self.assertRaises(WebDriverException):
            self.wait_for(self.browser.find_element_by_id('task0'))
        
        with self.assertRaises(WebDriverException):
            self.wait_for(self.browser.find_element_by_id('id_list0'))
        
        ##
        ## !! COPYPAST FROM ABOVE
        
        first_list_name = 'Zion'
        self.browser.get(self.tasks_url)
        self.wait_for(lambda: self.browser.find_element_by_id('list_form'))
        self.add_list(first_list_name)
        
        # check for this list
        list1 = self.wait_for(lambda: self.browser.find_element_by_id('id_list0'))
        self.assertTrue(list1.text == first_list_name)
        
        # add task
        first_task_name = 'GloryToAstortzka'
        self.add_task(first_task_name)
        
        # wait for task pop up
        task0 = self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        self.assertTrue(task0.text == first_task_name)
        
        # add another task
        second_task_name = 'Jesus'
        self.add_task(second_task_name)
        
        # wait for both tasks pop up and check them
        task0 = self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        task1 = self.browser.find_element_by_id('task1')
        self.assertTrue(task0.text == second_task_name)
        self.assertTrue(task1.text == first_task_name)
        
        # check that no another tasks
        with self.assertRaises(WebDriverException):
            self.browser.find_element_by_id('task2')
        with self.assertRaises(WebDriverException):
            self.browser.find_element_by_id('list1')
        
        # add second list
        second_list_name = 'Matix'
        self.add_list(second_list_name)
        
        # check for 2 lists
        list0 = self.wait_for(lambda: self.browser.find_element_by_id('id_list0'))
        list1 = self.browser.find_element_by_id('id_list1')
        self.assertTrue(list1.text == first_list_name)
        self.assertTrue(list0.text == second_list_name)
        
        # check tasks is empty
        with self.assertRaises(WebDriverException):
            self.wait_for(lambda: self.browser.find_element_by_id(first_task_name))
        with self.assertRaises(WebDriverException):
            self.browser.find_element_by_id(second_task_name)
        
        # add new task:
        third_task_name = 'Escape from matrix'
        self.add_task(third_task_name)
        
        # waif for task pop up and check it
        task3 = self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        self.assertTrue(task3.text == third_task_name)
        
        # one more check for tasks in another list:
        with self.assertRaises(WebDriverException):
            self.wait_for(lambda: self.browser.find_element_by_id('task1'))
        with self.assertRaises(WebDriverException):
            self.browser.find_element_by_id('task2')
        
        # switch to the first list:
        self.browser.find_element_by_id('id_list1').click()
        
        # check for two first tasks:
        task0 = self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        task1 = self.browser.find_element_by_id('task1')
        self.assertTrue(task1.text == first_task_name)
        self.assertTrue(task0.text == second_task_name)
        
        # check for 2 lists
        
        list1 = self.wait_for(lambda: self.browser.find_element_by_id('id_list1'))
        list0 = self.browser.find_element_by_id('id_list0')
        self.assertTrue(list1.text == first_list_name)
        self.assertTrue(list0.text == second_list_name)
        
        # check that third task is not exist here
        with self.assertRaises(WebDriverException):
            self.wait_for(lambda: self.browser.find_element_by_id(third_task_name))
    
    
    def test_check_for_non_existent_list(self):
        # try to open non-existing list
        self.browser.get(self.tasks_url + 'list42')
        
        # if tasklist is empty we are expecting a clear tasks page:
        header = self.wait_for(lambda: self.browser.find_element_by_id('header'))
        self.assertTrue(header.text == 'No task lists found! Maybe you should create one?')
        
        # so create a list and a couple tasks
        list1_name = 'Matrix'
        task1_name = 'Take red pill'
        task2_name = 'Escape from Matrix'
        
        self.add_list(list1_name)
        self.add_task(task1_name)
        self.add_task(task2_name)
        
        list2_name = 'Zion'
        task3_name = 'Arrive to Zion'
        task4_name = 'Save Zion from machines'
        
        self.add_list(list2_name)
        self.add_task(task3_name)
        self.add_task(task4_name)
        
        # try to open non-existing list again
        self.browser.get(self.tasks_url + 'list42')
        
        # expecting last created list
        header = self.wait_for(lambda: self.browser.find_element_by_id('header'))
        self.assertTrue(header.text == list2_name)
        
        # expecting our 3 last tasks
        task1 = self.browser.find_element_by_id('task0')
        task2 = self.browser.find_element_by_id('task1')
        
        self.assertTrue(task1.text == task3_name)
        self.assertTrue(task2.text == task4_name)
        
        # no other tasks
        with self.assertRaises(WebDriverException):
            self.browser.find_element_by_id('task2')
