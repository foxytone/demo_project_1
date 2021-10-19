from django.test import TestCase
from django.contrib.auth.models import User
from typing import Tuple, Dict
from ..models import List, Task


class BaseTest(TestCase):
    # Users
    # username, password
    MisterJones = {'username': 'MisterJones', 'password': 'MakeLoveNotWar1984'}
    Neo = {'username': 'Neo', 'password': 'ThereIsNoSp00n'}

    all_pattern = '(.|\n)'


    def setUp(self) -> None:
        self.register_user(self.MisterJones)
        self.register_user(self.Neo)


    def register_user(self, user: Dict[str, str]) -> None:
        new_user = User.objects.create(username=user['username'])
        new_user.set_password(user['password'])
        new_user.save()


    def login(self, user: Dict[str, str]) -> None:
        self.client.login(username=user['username'], password=user['password'])


    def create_new_list(self, listtext: str, user: Dict[str, str]) -> List:
        current_user = User.objects.get(username=user['username'])
        return List.objects.create(text=listtext, user=current_user)


    def create_new_task(self, tasktext: str, list_: List) -> Task:
        return Task.objects.create(text=tasktext, list=list_)


    def page_correct_tags(self, html: str) -> None:
        uni_pattern_for_pair_tags = '[^>]*>.*(.|\n)*</'

        self.assertTrue(html.startswith('<!DOCTYPE html>'), 'page doesnt start with DOCTYPE ')
        self.assertIn('<title>Tasks</title>', html)
        self.assertRegex(expected_regex=f'<html{uni_pattern_for_pair_tags}html>', text=html,
                         msg="can't find <html>")
        self.assertRegex(expected_regex=f'<body{uni_pattern_for_pair_tags}body>', text=html,
                         msg="cant find <body>")
        self.assertRegex(expected_regex=f'<h1{uni_pattern_for_pair_tags}h1>', text=html, msg="cant find header")
        self.assertRegex(expected_regex=f'<nav{uni_pattern_for_pair_tags}nav', text=html)
