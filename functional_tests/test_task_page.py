from .base import BaseTest
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


# TODO: add errors pop up and remove function for tasks and lists and limit for tasks and lists
class TestTaskPage(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        
        # init a user
        self.tasks_url = self.live_server_url + '/tasks/'
        self.register_user(self.MisterJones)
    
    
    def create_new_list(self, list_name: str) -> None:
        listbox = self.browser.find_element_by_id('list_form')
        self.send_info(listbox, list_name)
    
    
    def create_new_task(self, task_name: str) -> None:
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
        self.create_new_list(first_list_name)
        
        # check for this list
        list1 = self.wait_for(lambda: self.browser.find_element_by_id('id_list0'))
        self.assertTrue(list1.text == first_list_name + '\nX', list1.text)
        
        # add task
        first_task_name = 'My first task!'
        self.create_new_task(first_task_name)
        
        # wait for task pop up
        task0 = self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        self.assertIn(first_task_name, task0.text)
        
        # add another task
        second_task_name = 'My second task!'
        self.create_new_task(second_task_name)
        
        # wait for both tasks pop up and check them
        task0 = self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        task1 = self.browser.find_element_by_id('task1')
        self.assertIn(second_task_name, task0.text)
        self.assertIn(first_task_name, task1.text)
        
        # check that no another tasks
        with self.assertRaises(WebDriverException):
            self.browser.find_element_by_id('task2')
        with self.assertRaises(WebDriverException):
            self.browser.find_element_by_id('list1')
        
        # add second list
        second_list_name = 'My second list!'
        self.create_new_list(second_list_name)
        
        # check for 2 lists
        list0 = self.wait_for(lambda: self.browser.find_element_by_id('id_list0'))
        list1 = self.browser.find_element_by_id('id_list1')
        self.assertIn(first_list_name, list1.text)
        self.assertIn(second_list_name, list0.text)
        
        # check tasks is empty
        with self.assertRaises(WebDriverException):
            self.wait_for(lambda: self.browser.find_element_by_id(first_task_name))
        with self.assertRaises(WebDriverException):
            self.browser.find_element_by_id(second_task_name)
        
        # add new task:
        third_task_name = 'My third task!'
        self.create_new_task(third_task_name)
        
        # waif for task pop up and check it
        task3 = self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        self.assertIn(third_task_name, task3.text)
        
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
        self.assertIn(first_task_name, task1.text)
        self.assertIn(second_task_name, task0.text)
        
        # check for 2 lists
        
        list1 = self.wait_for(lambda: self.browser.find_element_by_id('id_list1'))
        list0 = self.browser.find_element_by_id('id_list0')
        self.assertIn(first_list_name, list1.text)
        self.assertIn(second_list_name, list0.text)
        
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
        self.create_new_list(first_list_name)
        
        # check for this list
        list1 = self.wait_for(lambda: self.browser.find_element_by_id('id_list0'))
        self.assertIn(first_list_name, list1.text)
        
        # add task
        first_task_name = 'GloryToAstortzka'
        self.create_new_task(first_task_name)
        
        # wait for task pop up
        task0 = self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        self.assertIn(first_task_name, task0.text)
        
        # add another task
        second_task_name = 'Jesus'
        self.create_new_task(second_task_name)
        
        # wait for both tasks pop up and check them
        task0 = self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        task1 = self.browser.find_element_by_id('task1')
        self.assertIn(second_task_name, task0.text)
        self.assertIn(first_task_name, task1.text)
        
        # check that no another tasks
        with self.assertRaises(WebDriverException):
            self.browser.find_element_by_id('task2')
        with self.assertRaises(WebDriverException):
            self.browser.find_element_by_id('list1')
        
        # add second list
        second_list_name = 'Matix'
        self.create_new_list(second_list_name)
        
        # check for 2 lists
        list0 = self.wait_for(lambda: self.browser.find_element_by_id('id_list0'))
        list1 = self.browser.find_element_by_id('id_list1')
        self.assertIn(first_list_name, list1.text)
        self.assertIn(second_list_name, list0.text)
        
        # check tasks is empty
        with self.assertRaises(WebDriverException):
            self.wait_for(lambda: self.browser.find_element_by_id(first_task_name))
        with self.assertRaises(WebDriverException):
            self.browser.find_element_by_id(second_task_name)
        
        # add new task:
        third_task_name = 'Escape from matrix'
        self.create_new_task(third_task_name)
        
        # waif for task pop up and check it
        task3 = self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        self.assertIn(third_task_name, task3.text)
        
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
        self.assertIn(first_task_name, task1.text)
        self.assertIn(second_task_name, task0.text)
        
        # check for 2 lists
        
        list1 = self.wait_for(lambda: self.browser.find_element_by_id('id_list1'))
        list0 = self.browser.find_element_by_id('id_list0')
        self.assertIn(first_list_name, list1.text)
        self.assertIn(second_list_name, list0.text)
        
        # check that third task is not exist here
        with self.assertRaises(WebDriverException):
            self.wait_for(lambda: self.browser.find_element_by_id(third_task_name))
    
    
    def test_check_for_non_existent_list(self):
        # try to open non-existing list
        self.browser.get(self.tasks_url + 'switch_list42')
        
        # if tasklist is empty we are expecting a clear tasks page:
        header = self.wait_for(lambda: self.browser.find_element_by_id('header'))
        self.assertTrue(header.text == 'No task lists found! Maybe you should create one?')
        
        # so create a list and a couple tasks
        list1_name = 'Matrix'
        task1_name = 'Take red pill'
        task2_name = 'Escape from Matrix'
        
        self.create_new_list(list1_name)
        self.create_new_task(task1_name)
        self.create_new_task(task2_name)
        
        list2_name = 'Zion'
        task3_name = 'Arrive to Zion'
        task4_name = 'Save Zion from machines'
        
        self.create_new_list(list2_name)
        self.create_new_task(task3_name)
        self.create_new_task(task4_name)
        
        # try to open non-existing list again
        self.browser.get(self.tasks_url + 'switch_list42')
        
        # expecting last created list
        header = self.wait_for(lambda: self.browser.find_element_by_id('header'))
        self.assertTrue(header.text == list2_name)
        
        # expecting our 3 last tasks
        task1 = self.browser.find_element_by_id('task0')
        task2 = self.browser.find_element_by_id('task1')
        
        self.assertIn(task4_name, task1.text)
        self.assertIn(task3_name, task2.text)
        
        # no other tasks
        with self.assertRaises(WebDriverException):
            self.browser.find_element_by_id('task2')
    
    
    def test_maximum_30_tasks(self):
        # create new list
        self.create_new_list('Matrix')
        
        # create 29 useless tasks
        
        for i in range(0, 29):
            self.create_new_task('task' + str(i))
        
        # check all 29 in list
        for i in range(0, 29):
            self.wait_for(lambda: self.browser.find_element_by_id('task' + str(i)))
        
        # add 30th task
        self.create_new_task('task42')
        
        # check all is good
        self.wait_for(lambda: self.browser.find_element_by_id('task29'))
        
        # try to add another task
        self.create_new_task('task43')
        
        # and cant find it in list
        with self.assertRaises(WebDriverException):
            self.wait_for(lambda: self.browser.find_element_by_id('task30'))
        
        # but error is right here
        error = self.browser.find_element_by_id('error_1_id_text')
        self.assertTrue(error.text == "You've reached maximum tasks of 30. Delete one for adding new task")
        
        self.browser.get(self.tasks_url)
        # and here must be 2 errors
        self.create_new_task('task20')
        error1 = self.wait_for(lambda: self.browser.find_element_by_id('error_1_id_text'))
        error2 = self.browser.find_element_by_id('error_2_id_text')
        
        self.assertTrue(error1.text == "You already have this task")
        self.assertTrue(error2.text == "You've reached maximum tasks of 30. Delete one for adding new task")
    
    
    def test_cant_create_empty_list(self):
        self.browser.get(self.tasks_url)
        
        self.create_new_list('')
        
        with self.assertRaises(WebDriverException):
            self.wait_for(lambda: self.browser.find_element_by_id('id_list0'))
    
    
    def test_cant_create_empty_task(self):
        self.browser.get(self.tasks_url)
        
        self.create_new_list('Matrix')
        
        with self.assertRaises(WebDriverException):
            self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        
        self.create_new_task('')
        
        with self.assertRaises(WebDriverException):
            self.wait_for(lambda: self.browser.find_element_by_id('task0'))
    
    
    def test_cant_create_duplicated_lists(self):
        self.browser.get(self.tasks_url)
        
        with self.assertRaises(WebDriverException):
            self.browser.find_element_by_id('id_list0')
        
        self.create_new_list('Matrix')
        
        self.wait_for(lambda: self.browser.find_element_by_id('id_list0'))
        with self.assertRaises(WebDriverException):
            self.browser.find_element_by_id('id_list1')
        
        self.create_new_list('Matrix')
        
        with self.assertRaises(WebDriverException):
            self.wait_for(lambda: self.browser.find_element_by_id('id_list1'))
        
        error = self.browser.find_element_by_id('error_1_id_text')
        self.assertTrue(error.text == "You already have this list", error.text)
    
    
    def test_cant_create_duplicated_tasks(self):
        self.browser.get(self.tasks_url)
        
        # create new list and check for no tasks there
        self.create_new_list('Matrix')
        with self.assertRaises(WebDriverException):
            self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        
        self.create_new_task('task')
        
        # wait for task pop up
        self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        
        # create duplicated task
        self.create_new_task('task')
        
        # check it is not there
        with self.assertRaises(WebDriverException):
            self.wait_for(lambda: self.browser.find_element_by_id('task1'))
        
        # check for error
        error = self.browser.find_element_by_id('error_1_id_text')
        self.assertTrue(error.text == "You already have this task", error.text)
    
    
    def test_maximum_20_lists(self):
        # create 19 useless lists
        for i in range(0, 19):
            self.create_new_list('list' + str(i))
        
        # check all 19 in list
        for i in range(0, 19):
            self.wait_for(lambda: self.browser.find_element_by_id('id_list' + str(i)))
        
        # add 20th list
        self.create_new_list('list42')
        
        # check all is good
        self.wait_for(lambda: self.browser.find_element_by_id('id_list19'))
        
        # try to add another task
        self.create_new_list('list43')
        
        # and cant find it in list
        with self.assertRaises(WebDriverException):
            self.wait_for(lambda: self.browser.find_element_by_id('id_list20'))
        
        # but error is right here
        error = self.browser.find_element_by_id('error_1_id_text')
        self.assertTrue(error.text == "You've reached maximum lists of 20. Delete one for adding new list")
        
        self.browser.get(self.tasks_url)
        # and here must be 2 errors
        self.create_new_list('list10')
        error1 = self.wait_for(lambda: self.browser.find_element_by_id('error_1_id_text'))
        error2 = self.browser.find_element_by_id('error_2_id_text')
        
        self.assertTrue(error1.text == "You already have this list")
        self.assertTrue(error2.text == "You've reached maximum lists of 20. Delete one for adding new list")
    
    
    def test_lists_removes_correctly(self):
        self.browser.get(self.tasks_url)
        
        # create a new list and remove it
        self.create_new_list('One')
        button = self.wait_for(lambda: self.browser.find_element_by_id('remove_list_button0'))
        button.click()
        
        # check all is good
        header = self.wait_for(lambda: self.browser.find_element_by_id('header'))
        self.assertTrue(header.text == "No task lists found! Maybe you should create one?")
        
        # create same list
        self.create_new_list('One')
        list_name = self.wait_for(lambda: self.browser.find_element_by_id('id_list0'))
        self.assertTrue(list_name.text == 'One\nX')
        
        # create few tasks
        task1 = 'Take red pill'
        task2 = 'Return to farm'
        
        self.create_new_task(task1)
        self.create_new_task(task2)
        
        # check all tasks in the list
        t1 = self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        t2 = self.browser.find_element_by_id('task1')
        
        self.assertIn(task2, t1.text)
        self.assertTrue(task1, t2.text)
        
        # remove this list
        self.browser.find_element_by_id('remove_list_button0').click()
        
        # create same list again
        self.create_new_list('One')
        
        # no tasks there
        with self.assertRaises(WebDriverException):
            self.wait_for(lambda: self.browser.find_element_by_id('task0'))
    
    
    def test_cant_remove_non_existing_task(self):
        self.browser.get(self.tasks_url + 'remove_task20')
        header = self.wait_for(lambda: self.browser.find_element_by_id('header'))
        self.assertTrue(header.text == "No task lists found! Maybe you should create one?")
    
    
    def test_task_remove(self):
        # create a new list
        self.create_new_list('Matrix')
        
        # add few tasks
        task1_name = 'Zion'
        task2_name = 'Farm'
        task3_name = 'task 3'
        
        self.create_new_task(task1_name)
        self.create_new_task(task2_name)
        self.create_new_task(task3_name)
        
        # remove 2nd task
        
        remove_button = self.wait_for(lambda: self.browser.find_element_by_id('remove_task_button1'))
        remove_button.click()
        
        task0 = self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        task1 = self.browser.find_element_by_id('task1')
        
        # check for tasks
        
        self.assertIn(task3_name, task0.text)
        self.assertIn(task1_name, task1.text)
        
        # checkout list
        
        self.create_new_list('Farm')
        
        # create another tasks
        
        task4_name = 'task4'
        task5_name = 'task5'
        task6_name = 'task6'
        
        self.create_new_task(task4_name)
        self.create_new_task(task5_name)
        self.create_new_task(task6_name)
        
        task0 = self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        task1 = self.browser.find_element_by_id('task1')
        task2 = self.browser.find_element_by_id('task2')
        
        self.assertIn(task6_name, task0.text)
        self.assertIn(task5_name, task1.text)
        self.assertIn(task4_name, task2.text)
        
        # remove them all
        
        for i in range(0, 3):
            remove_button = self.wait_for(lambda: self.browser.find_element_by_id('remove_task_button0'))
            remove_button.click()
        
        # check for no tasks
        with self.assertRaises(WebDriverException):
            self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        
        # checkout to first list
        
        self.browser.find_element_by_id('id_list1').click()
        
        # check our first tasks still here
        
        task0 = self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        task1 = self.browser.find_element_by_id('task1')
        
        # check for tasks
        
        self.assertIn(task3_name, task0.text)
        self.assertIn(task1_name, task1.text)
    
    
    def test_cant_remove_non_existing_list(self):
        self.browser.get(self.tasks_url)
        self.browser.get(self.tasks_url + 'remove_list12')
        header = self.wait_for(lambda: self.browser.find_element_by_id('header'))
        self.assertTrue(header.text == "No task lists found! Maybe you should create one?")
    
    
    def test_marked_tasks(self):
        self.create_new_list('Matrix')
        
        # few tasks
        
        task1_name = 'task1'
        task2_name = 'task2'
        task3_name = 'task3'
        
        self.create_new_task(task1_name)
        self.create_new_task(task2_name)
        self.create_new_task(task3_name)
        
        self.wait_for(lambda: self.browser.find_element_by_id('mark_task_button1')).click()
        
        task0 = self.wait_for(lambda: self.browser.find_element_by_id('task0'))
        task1 = self.browser.find_element_by_css_selector('s')
        task2 = self.browser.find_element_by_id('task2')
        
        self.assertIn(task3_name, task0.text)
        self.assertTrue(task2_name == task1.text, task1.text)
        self.assertIn(task1_name, task2.text)
        
        self.browser.find_element_by_id('mark_task_button1').click()
        with self.assertRaises(WebDriverException):
            self.wait_for(lambda: self.browser.find_element_by_css_selector('s'))
