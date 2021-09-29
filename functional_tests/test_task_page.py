from .base import BaseTest


class TaskPageTest(BaseTest):
    def test_can_add_a_task(self):
        self.browser.get(self.live_server_url + '/tasks/')
        inputbox = self.browser.find_element_by_id(id_='task_form')
        task_one = 'Make a task list!'
        self.send_info(inputbox, task_one)
        self.wait_for_row_in_list_table(task_one)